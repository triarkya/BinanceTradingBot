# BinanceTradingBot

#### (Note: currently only for USDT as quote asset and market buy/sell only!)

[Register on Binance](https://www.binance.com/en/register?ref=23830900)

## Features

- easy and fast configuration (edit lib/conf.py) (Note: usage of BTC as quote asset not implemented yet)

	|attribute in conf.py| desription |
	---------------------|------------|
	| binance\_apikey/ binance\_apisecret | Binance API keys |
	| candle\_interval | candlestick interval (15 minutes by default) |
	| coins\_to\_ignore | list of symbols to ignore (e.g. "BTCUSDT") |
	| coins\_to\_include | list of symbols to trade even though maybe not enough volume |
	| minvolume\_USDT | minimum trading volume for symbols with USDT as quote asset |
	| minvolume\_BTC | minimum trading volume for symbols with BTC as quote asset |
	| totalasset\_USDT | how much USDT you have to use as quote asset |
	| totalasset\_BTC | how much BTC you have to use as quote asset |
	| perc\_per\_trade | how many percent of your quote asset you want to invest per trade? (Note: 0.09 = 9%) |
	| minvalue\_USDT | how much of USDT should be invested per trade even though there is not enough available USDT in percentage terms? |
	| minvalue\_BTC | how much of BTC should be invested per trade even though there is not enough available BTC in percentage terms? |
	| notify\_telegram | set this to true if you want to be notified after buy/sell |
	| tgbot\_apikey | Telegram API key ([BotFather TelegramBot](https://t.me/BotFather)) |
	| tgchat_id | the chat id of the Telegram chat which gets the notifications

- run the bot precisely at specific time (like Cronjob)

- set custom strategy to enter and exit long position
    - use TA-Lib indicators (see all indicators on TA-Lib git)
    - use custom indicators (just modify indicators.py :])
    - to use an indicator, add your indicator to the add_indicators method in lib/Symbol.py
- keep a record of every executed trade (buy, sell, profit)
    
    ***results/trades.csv***:
    > name;symbol;{price: qty};avg_price
    
    ***results/executed\_sell\_trades.csv***:
    > name,time,buy\_qty,sell\_qty,percent\_profit,stable\_profit
    
    ***results/profit.csv***:
    > name,profit
    
- get Telegram notification after every executed trade

## Additional Indicators

- Middle (average of High, Low, Open, Close)
- VWMA (Volume Weighted Moving Average)
- RVGI (Relative Vigor Index + RVGI Signal)
- Supertrend
 
## Used Libraries

[apscheduler](https://github.com/agronholm/apscheduler)

[pandas](https://github.com/pandas-dev/pandas)

[numpy](https://github.com/numpy/numpy)

[python-binance](https://github.com/sammchardy/python-binance)

[TA-Lib](https://github.com/mrjbq7/ta-lib)

[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Disclaimer

I am not responsible for anything done with this trading bot. You use it at your own risk. There are no warranties or guarantees expressed or implied. You assume all responsibility and liability.