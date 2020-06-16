import pandas as pd
import numpy as np


# calculates the average of values for a specififc subinterval from a list of numeric values
# returns generator object (cast to list etc.)
def values_to_avg(values, interval):
    for i in range(1, len(values) + 1):
        if len(values[:i]) < interval:
            yield sum(values[:i]) / len(values[:i])
        else:
            yield sum(values[i - interval:i]) / len(values[i - interval:i])


# calculates the average of open, high, low and close
def Middle(df):
    return (df["open"] + df["high"] + df["low"] + df["close"]) / 4


# calculates volume weighted moving average for an indicator (close by default)
# and time interval (14 steps by default)
def VWMA(df, indicator="close", interval=14):
    vwma = []
    pv = []
    for i in range(len(df)):
        pv.append(df[indicator][i] * df["volume"][i])
        if i // interval == 0:
            if sum(df["volume"][:i + 1]) == 0:
                vwma.append(df[indicator][i])
            else:
                vwma.append(sum(pv) / sum(df["volume"][:i + 1]))
        else:
            if sum(df["volume"][i - interval:i + 1]) == 0:
                vwma.append(df[indicator][i])
            else:
                vwma.append(sum(pv[i - interval:i + 1]) / sum(df["volume"][i - interval:i + 1]))
    return vwma


# calculates relative vigor index (+ relative vigor index signal)
# time interval by default 10 steps
def RVGI(df, interval=10):
    close_open = list(df['close'] - df['open'])
    high_low = list(df['high'] - df['low'])
    numerator = np.array([])
    denominator = np.array([])
    for i in range(len(close_open)):
        if i >= 3:
            numerator = np.append(
                numerator,
                (close_open[i] + 2 * close_open[i - 1] + 2 * close_open[i - 2] + close_open[
                    i - 3]) / 6
            )
            denominator = np.append(
                denominator,
                (high_low[i] + 2 * high_low[i - 1] + 2 * high_low[i - 2] + high_low[i - 3]) / 6
            )
        elif i == 2:
            numerator = np.append(
                numerator,
                (close_open[i] + 2 * close_open[i - 1] + 2 * close_open[i - 2]) / 5
            )
            denominator = np.append(
                denominator,
                (high_low[i] + 2 * high_low[i - 1] + 2 * high_low[i - 2]) / 5
            )
        elif i == 1:
            numerator = np.append(
                numerator,
                (close_open[i] + 2 * close_open[i - 1]) / 3
            )
            denominator = np.append(
                denominator,
                (high_low[i] + 2 * high_low[i - 1]) / 3
            )
        elif i == 0:
            numerator = np.append(
                numerator,
                close_open[i]
            )
            denominator = np.append(
                denominator,
                high_low[i]
            )
    rvgi = list(values_to_avg(numerator / denominator, interval))
    rvgi_signal = []

    for i in range(len(rvgi)):
        if i >= 3:
            rvgi_signal.append(
                (rvgi[i] + 2 * rvgi[i - 1] + 2 * rvgi[i - 2] + rvgi[i - 3]) / 6
            )
        elif i == 2:
            rvgi_signal.append(
                (rvgi[i] + 2 * rvgi[i - 1] + 2 * rvgi[i - 2]) / 5
            )
        elif i == 1:
            rvgi_signal.append(
                (rvgi[i] + 2 * rvgi[i - 1]) / 3
            )
        elif i == 0:
            rvgi_signal.append(
                rvgi[i]
            )

    return rvgi, rvgi_signal


# calculates Supertrend
# time interval by default 10 steps, factor by default 2
def Supertrend(df, factor=2, interval=10):
    high = df["high"].tolist()
    low = df["low"].tolist()
    close = df["close"].tolist()
    atr = df["atr"].tolist()

    basic_upperband = ((np.array(high) + np.array(low)) / factor) + factor * np.array(atr)
    basic_lowerband = ((np.array(high) + np.array(low)) / factor) - factor * np.array(atr)

    final_upperband = [0.0]
    final_lowerband = [basic_lowerband[0]]
    for i in range(1, len(basic_upperband)):
        if basic_upperband[i] < final_upperband[i - 1] or close[i - 1] > final_upperband[i - 1]:
            final_upperband.append(basic_upperband[i])
        else:
            final_upperband.append(final_upperband[i - 1])
        if basic_lowerband[i] > final_lowerband[i - 1] or close[i - 1] < final_lowerband[i - 1]:
            final_lowerband.append(basic_lowerband[i])
        else:
            final_lowerband.append(final_lowerband[i - 1])

    supertrend = [final_upperband[0] if close[0] < final_upperband[0] else final_lowerband[0]]
    for j in range(1, len(close)):
        try:
            if supertrend[j - 1] == final_upperband[j - 1]:
                if close[j] <= final_upperband[j]:
                    supertrend.append(final_upperband[j])
                elif close[j] > final_upperband[j]:
                    supertrend.append(final_lowerband[j])
            elif supertrend[j - 1] == final_lowerband[j - 1]:
                if close[j] >= final_lowerband[j]:
                    supertrend.append(final_lowerband[j])
                elif close[j] < final_lowerband[j]:
                    supertrend.append(final_upperband[j])
        except IndexError:
            print("IndexError " + str(j))
    return supertrend
