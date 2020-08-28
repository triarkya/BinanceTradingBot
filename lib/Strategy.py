from lib.Symbol import Symbol


class Strategy:
    def __init__(self, symbol='BTCUSDT'):
        self.symbol = Symbol(symbol)
        self.is_hot_buy = self.long_enter()
        self.is_hot_sell = self.long_exit()
        self.enough_data = self.symbol.enough_data

    # edit this method to set your strategy to enter a long trade
    def long_enter(self):
        if self.symbol.df['close'].tolist()[-1] > self.symbol.df['open'].tolist()[-1]:
            if 1 < 0:
                return True

    # edit this method to set your strategy to exit a long trade
    def long_exit(self):
        if self.symbol.df['di_neg'].tolist()[-1] >= 20 and self.symbol.df['adx'].tolist()[-1] >= 25:
            if 1 < 0:
                return True
