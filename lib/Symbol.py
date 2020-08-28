import pandas as pd
import lib.conf as conf
from binance.client import Client
from talib.abstract import *
from lib.indicators import *


# convert date to seconds and set every relevant non-float column to float
def only_numlist(candle_elem):
    return [candle_elem[0] // 1000] + [float(val) if type(val) is str else val for val in candle_elem[1:6]]


class Symbol:
    def __init__(self, name='BTCUSDT'):
        # set the basic information
        self.name = name
        self.client = Client(
            api_key=conf.binance_apikey,
            api_secret=conf.binance_apisecret
        )
        self.interval = eval('self.client.KLINE_INTERVAL_' + conf.candle_interval)
        self.symbol_info = self.client.get_symbol_info(name)
        self.lot_size = self.symbol_info['filters'][2]['stepSize'].find('1') - 1
        self.enough_data = False

        # get all relevant columns as candle_df_raw
        candles_get = self.client.get_historical_klines(
            self.name,
            self.interval,
            "8 days ago UTC"
        )
        candles_data = [only_numlist(candle) for candle in candles_get]
        candles_df_raw = pd.DataFrame(candles_data)
        candles_df_raw.columns = ["date", "open", "high", "low", "close", "volume"]
        candles_df_raw["date"] = candles_df_raw["date"] / 1000
        self.df = candles_df_raw
        self.add_indicators()

    def add_indicators(self):
        inputs = {
            'open': self.df['open'],
            'high': self.df['high'],
            'low': self.df['low'],
            'close': self.df['close'],
            'volume': self.df['volume'],
        }

        # uppercase indicators are from ta-lib
        self.df["middle"] = (self.df["high"] + self.df["low"] + self.df["close"] + self.df["open"]) / 4
        self.df["ema_25"] = EMA(inputs, timeperiod=25)
        self.df["wma_50"] = WMA(inputs, timeperiod=50)
        self.df["wma_100"] = WMA(inputs, timeperiod=100)
        self.df["wma_200"] = WMA(inputs, timeperiod=200)
        self.df["macd"], self.df["macds"], self.df["macdh"] = MACD(inputs)
        self.df["mfi"] = MFI(inputs)
        self.df["adx"] = ADX(inputs, timeperiod=14)
        self.df["di_neg"] = MINUS_DI(inputs, timeperiod=14)
        self.df["di_pos"] = PLUS_DI(inputs, timeperiod=14)
        self.df["atr"] = ATR(inputs, timeperiod=10)
        self.df["chaikin_osc"] = ADOSC(inputs)
        self.df["ultimate_osc"] = ULTOSC(inputs)
        self.df = self.df.dropna()
        self.df["supertrend"] = Supertrend(self.df, 2, 10)
        self.df["rvgi"], self.df["rvgi_signal"] = RVGI(self.df, 10)
