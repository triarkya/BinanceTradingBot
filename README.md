# BinanceTradingBot

## Note

- currently only for USDT as quote asset and market buy/sell only!

[Register on Binance](https://www.binance.com/en/register?ref=23830900)

## Features

- easy and fast configuration (edit conf.py)
    - Binance API keys
    - candlestick interval (15 minutes by default)
    - set a minimum 24h trade volume (below will be ignored)
    - which specific coins/pairs shoud be ignored or included?
    - how many percent of your total asset you want to invest per trade
    - the minimum amount to be invested per trade

- run the bot precisely at specific time (like Cronjob)

- set custom strategy to enter and exit long position
    - use TA-Lib indicators (see all indicators on TA-Lib git)
    - use custom indicators (just modify indicators.py :])
    - to use an indicator, add your indicator to the add_indicators method in lib/Symbol.py
- keep a record of every executed trade (buy, sell, profit)
    
    ***trades.csv***:
    > name;symbol;{price: qty};avg_price
    
    ***executed\_sell\_trades.csv***:
    > name,time,buy\_qty,sell\_qty,percent\_profit,stable\_profit
    
    ***profit.csv***:
    > name,profit
    
- get telegram notification after every executed trade

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