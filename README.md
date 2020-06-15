# BinanceTradingBot

## Note

- currently only for USDT as quote asset and market buy/sell only!
- current state of Bot not executable, still in progress

## Features

- easy and fast configuration (edit conf.py)
    - Binance API keys
    - candlestick interval (15 minutes by default)
    - set a minimum 24 trade volume (below will be ignored)
    - how many percent of your total asset you want to invest per trade
    - the minimum amount to be invested per trade
- run the Bot precisely at specific time (like Cronjob)
- set custom strategy to enter and exit long position
    - use TA-Lib indicators (see all indicators on TA-Lib git)
- get telegram notification after every executed trade
 
## Used Libraries

apscheduler: https://github.com/agronholm/apscheduler

pandas: https://github.com/pandas-dev/pandas

python-binance: https://github.com/sammchardy/python-binance

TA-Lib: https://github.com/mrjbq7/ta-lib

python-telegram-bot: https://github.com/python-telegram-bot/python-telegram-bot