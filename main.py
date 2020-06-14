import pandas as pd
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from lib.BinanceAccount import BinanceAccount
import lib.conf as conf


def session():
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S,%f"))
    client = BinanceAccount()

    '''
        get ticker data of market
        symbol_prices:    'BTCUSDT': xxxx.xx
    '''
    ticker_df = pd.DataFrame(client.client.get_ticker())
    symbol_prices = {}
    for pair_price in client.client.get_all_tickers():
        symbol_prices[pair_price['symbol']] = float(pair_price['price'])

    '''
        only pairs with USDT
        only pairs with volume > minimal volume of interest to trade
        only pairs not containing other quote asset than USDT
    '''
    filter_ticker_df = ticker_df['symbol'].str.contains('USDT')
    ticker_df = ticker_df[filter_ticker_df]
    filter_ticker_df = ticker_df['quoteVolume'].astype(float) > conf.minvolume_USDT
    ticker_df = ticker_df[filter_ticker_df]
    ignore_coins = ['USDC', 'PAX', 'BUSD', 'TUSD', 'USDS', 'BNB', 'MTL'] + conf.coins_to_ignore
    for coin in ignore_coins:
        filter_ticker_df = ticker_df['symbol'].str.contains(coin)
        ticker_df = ticker_df[~filter_ticker_df]

    trade_pairs = ticker_df['symbol'].tolist()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(session, 'cron', minute=0, second=5)
    scheduler.add_job(session, 'cron', minute=15, second=5)
    scheduler.add_job(session, 'cron', minute=30, second=5)
    scheduler.add_job(session, 'cron', minute=45, second=5)
    scheduler.start()