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

    # calculates the quote asset value per executed trade
    def set_value_per_trade(self):
        if self.quote_funds * conf.perc_per_trade >= eval(f'conf.minvalue_{self.quote}'):
            return self.quote_funds * conf.perc_per_trade
        return eval(f'conf.minvalue_{self.quote}')

    # returns the total quote asset balance (for example USDT)
    def return_balance(self, quote):
        return float(self.client.get_asset_balance(asset=quote)['free'])

    # execute market buy order
    def start_buy_order(self, symbol, latest_price, lot_filter):
        # only trade if enough funds!
        if self.current_quote_funds > self.value_per_trade:
            qty = round(self.value_per_trade / latest_price, lot_filter)
            buy = self.client.order_market_buy(
                symbol=symbol,
                quantity=qty
            )
            print(self.name, 'bought', qty, symbol)
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

    # execute market sell order
    def start_sell_order(self, symbol, latest_price, lot_filter):
        symbol_balance = self.return_balance(quote=symbol[:-4])
        if symbol_balance * latest_price > 11:
            qty = round(int(symbol_balance * (10 ** lot_filter)) / (10 ** lot_filter), lot_filter)
            sell = self.client.order_market_sell(
                symbol=symbol,
                quantity=qty
            )
            time.sleep(0.2)
            sell_qty = float(sell['cummulativeQuoteQty'])
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
