from binance.client import Client
import time
import telegram
import lib.conf as conf


class BinanceAccount:
    def __init__(self, quote='USDT'):
        self.name = conf.name
        self.client = Client(api_key=conf.binance_apikey, api_secret=conf.binance_apisecret)
        self.quote = quote
        self.quote_funds = 300 if quote == 'USDT' else 0.05  # method to get the data will be added later
        self.value_per_trade = self.set_value_per_trade()
        self.current_quote_funds = self.return_balance(quote)

    # keep a record of every trade in trades.csv
    # name;symbol;{price: qty};avg_price
    def trade_to_csv(self, symbol, price, quote_qty):
        lines = []
        try:
            trades_file = open('trades.csv', 'r')
            lines = trades_file.read().splitlines()
            trades_file.close()
        except FileNotFoundError:
            print("no trades.csv found")

        symbol_in_trades = False
        if len(lines) > 0:
            for line in lines:
                name, pair, priceqty, avg = line.rstrip().split(';')
                if pair == symbol and name == self.name:
                    symbol_in_trades = True
                    lines.remove(line)
                    priceqty = eval(priceqty)
                    priceqty[price] = quote_qty
                    avg = 0

                    # price, balance
                    for p, b in priceqty.items():
                        # calculate weighted average buy price
                        avg += p * b / sum(priceqty.values())
                    new_line = ';'.join([self.name, pair, str(priceqty), str(avg)])
                    lines.append(new_line)
                    break

            if not symbol_in_trades:
                new_line = ';'.join([self.name, symbol, str({price: quote_qty}), str(price)])
                lines.append(new_line)

        else:
            lines = [';'.join([self.name, symbol, str({price: quote_qty}), str(price)])]
        new_trades_file = open('trades.csv', 'w')
        new_trades_file.write('\n'.join(lines))
        new_trades_file.close()

    # calculates the quote asset value per executed trade
    def set_value_per_trade(self):
        if self.quote_funds * conf.perc_per_trade >= eval(f'conf.minvalue_{self.quote}'):
            return self.quote_funds * conf.perc_per_trade
        return eval(f'conf.minvalue_{self.quote}')

    # returns the total quote asset balance (for example USDT)
    def return_balance(self, quote):
        return float(self.client.get_asset_balance(asset=quote)['free'])

    # execute market buy order
    def start_market_buy(self, symbol, latest_price, lot_filter):
        # only trade if enough funds!
        if self.current_quote_funds > self.value_per_trade:
            qty = round(self.value_per_trade / latest_price, lot_filter)
            buy = self.client.order_market_buy(
                symbol=symbol,
                quantity=qty
            )
            if conf.notify_telegram:
                message = self.name + ' bought #' + symbol
                tgb = telegram.Bot(token=conf.tgbot_apikey)
                try:
                    tgb.send_message(
                        conf.tgchat_id,
                        message,
                        parse_mode='Markdown',
                        disable_web_page_preview=True
                    )
                except:
                    print("Connection Error\n")

            time.sleep(0.2)
            print(self.name, 'bought', qty, symbol)
            quote_qty = float(buy['cummulativeQuoteQty'])
            asset_qty = float(buy['executedQty'])
            price = 0
            for fill in buy['fills']:
                price += float(fill['price']) * float(fill['qty']) / asset_qty
            self.trade_to_csv(
                symbol=symbol,
                price=price,
                quote_qty=float(quote_qty),
            )

    # execute market sell order
    def start_market_sell(self, symbol, latest_price, lot_filter):
        symbol_balance = self.return_balance(quote=symbol[:-4])
        # because lower order limit is 10 USDT
        if symbol_balance * latest_price > 11:
            priceqty_pair = 0
            qty = round(int(symbol_balance * (10 ** lot_filter)) / (10 ** lot_filter), lot_filter)
            sell = self.client.order_market_sell(
                symbol=symbol,
                quantity=qty
            )

            # update trades.csv
            tradesfile = open('trades.csv', 'r')
            lines = tradesfile.read().splitlines()
            tradesfile.close()
            for line in lines:
                name, pair, priceqty_pair, avg = line.rstrip().split(';')
                if pair == symbol and name == self.name:
                    lines.remove(line)
                    break
            tradesfile = open('trades.csv', 'w')
            tradesfile.writelines('\n'.join(lines))
            tradesfile.close()

            # send telegram bot message
            sell_qty = float(sell['cummulativeQuoteQty'])
            buy_qty = sum(eval(priceqty_pair).values())
            profit = sell_qty - buy_qty
            message = self.name + ' sold #' + str(sell_qty) + " " + symbol
            print(message)
            if conf.notify_telegram:
                tgb = telegram.Bot(token=conf.bot_apikey)
                try:
                    tgb.send_message(
                        conf.tgchat_id,
                        message,
                        parse_mode='Markdown',
                        disable_web_page_preview=True
                    )
                except:
                    print("Connection Error\n")

            # note down all new profits in executed_sell_trades.csv
            sell_profit_file = open('executed_sell_trades.csv', 'r')
            executed_trades = sell_profit_file.read().splitlines()
            sell_profit_file.close()
            executed_trades.append(','.join(
                [
                    self.name,
                    str(sell['transactTime']),
                    str(buy_qty),
                    str(sell_qty),
                    str(((sell_qty / buy_qty) - 1) * 100),
                    str(sell_qty - buy_qty)
                ]
            ))
            sell_profit_file = open('executed_sell_trades.csv', 'w')
            sell_profit_file.write('\n'.join(executed_trades))
            sell_profit_file.close()

            # update profit.csv for account
            profit_file = open('profit.csv', 'r')
            all_profits = profit_file.read().splitlines()
            profit_file.close()
            for profit_line in all_profits:
                name, full_profit = profit_line.rstrip().split(',')
                if name == self.name:
                    all_profits.remove(profit_line)
                    full_profit = float(full_profit)
                    full_profit += profit
                    all_profits.append(','.join([name, str(full_profit)]))
                    profit_file = open('profit.csv', 'w')
                    profit_file.write('\n'.join(all_profits))
                    profit_file.close()
                    break
