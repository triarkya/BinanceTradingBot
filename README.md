# BinanceTradingBot

#### (Note: currently only for USDT as quote asset and market buy/sell only!)

[Register on Binance](https://www.binance.com/en/register?ref=23830900)

## Features

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

## Configuration 

- easy and fast configuration (edit lib/settings.json) 
- (Note: usage of BTC as quote asset not implemented yet)
	
	### BinanceSettings
	
	`BinanceSettings` properties
	
	|property name| desription |
	|---------------------|------------|
	| Account | settings to use your Binance account |
	| Exchange | settings for candle interval etc. |
	| Filter | settings to filter the ticker data |
	| TradeParameters | parameters how risky you want to trade | 
	
	#### `BinanceSettings.Account`
	
	settings to use your Binance account
	
	- **Name**: your name ("admin" per default)
	- **Total\_USDT**: how much USDT you have to use as quote asset
	- **API\_Key**: your Binance API Key
	- **API\_Secret**: your Binance API Secret

	#### `BinanceSettings.Exchange`
	
	settings for candle interval etc.
	
	- **Candle\_Interval**: the candle interval for the historical klines ("15MINUTE" per default)

	#### `BinanceSettings.Filter`
	
	settings to filter the ticker data
	
	- **Coins\_to\_ignore**: list of symbols to ignore (e.g. "BTCUSDT")
	- **Coins\_to\_include**: list of symbols to trade even though maybe not enough volume
	- **Min\_Volume\_USDT**: minimum trading volume for symbols with USDT as quote asset

	#### `BinanceSettings.TradeParameters`
	
	parameters how risky you want to trade
	
	- **Percent\_per\_Trade**: how many percent of your quote asset you want to invest per trade? (Note: 0.09 = 9%)
	- **MinValue\_USDT**: how much of USDT should be invested per trade even though there is not enough available USDT in percentage terms? 
	
	### NotificationSettings
	
	`NotificationSettings` properties
	
	|property name| desription |
	|---------------------|------------|
	| Telegram | settings to get notifications in Telegram|
	
	#### `NotificationSettings.Telegram`
	
	settings to get notifications in Telegram
	
	- **Get\_Notification**: set this to true if you want to be notified after buy/sell
	- **Bot\_API\_Key**: Telegram Bot API key ([BotFather TelegramBot](https://t.me/BotFather))
	- **Chat\_ID**: the chat ID of the Telegram chat which gets the notifications

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