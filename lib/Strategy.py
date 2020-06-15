from lib.Symbol import Symbol


class Strategy:
    def __init__(self, symbol='BTCUSDT'):
        self.symbol = Symbol(symbol)
        self.is_hot_buy = self.long_enter()
        self.is_hot_sell = self.long_exit()
        self.checkable = self.symbol.enough_data

    # edit this method to set your strategy to enter a long trade
    def long_enter(self):
        if self.symbol.df['close'] > self.symbol.df['open']:
            return True

    # edit this method to set your strategy to exit a long trade
    def long_exit(self):
        if self.symbol.df['di_neg'] >= 20 and self.symbol.df['adx'] >= 25:
            return True
