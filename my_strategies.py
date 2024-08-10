from backtesting import Backtest, Strategy
import pandas as pd
import talib
from backtesting.lib import crossover
#

def custom_ind(indicator):
    """ use to create a custom indicator"""
    return indicator
################### MACD crossover #######################################################################################################################
class MACDStrategy(Strategy):
    # MACD default parameters
    fastperiod = 12
    slowperiod = 26
    signalperiod = 9
    
    def init(self):
        # Compute MACD and MACD Signal
        macd, macdsignal, macdhist = self.I(talib.MACD, self.data['Adj Close'], 
                                            fastperiod=self.fastperiod, 
                                            slowperiod=self.slowperiod, 
                                            signalperiod=self.signalperiod)
        self.macd = macd
        self.macdsignal = macdsignal

        # Compute 20-day and 100-day EMA
        self.ema20 = self.I(talib.EMA, self.data['Adj Close'], timeperiod=20)
        self.ema100 = self.I(talib.EMA, self.data['Adj Close'], timeperiod=100)

    def next(self):
        if (crossover(self.macd, self.macdsignal) and 
            self.ema20[-1] > self.ema100[-1]):
            self.buy()

        if (crossover(self.macdsignal, self.macd) or 
            self.ema20[-1] < self.ema100[-1]):
            self.position.close()
####################### RSI with low volatility##########################################################################################################
class ATRRSIStrategy(Strategy):
    atr_short_period = 14
    atr_long_period = 100
    buy_threshold = 30
    sell_threshold = 70

    def init(self):
        # Initialize RSI
        self.rsi = self.I(talib.RSI, self.data['Adj Close'], timeperiod=14)
        # Initialize ATR
        self.atr_short = self.I(talib.ATR, self.data['High'], self.data['Low'], self.data['Adj Close'], timeperiod=self.atr_short_period)
        self.atr_long = self.I(talib.ATR, self.data['High'], self.data['Low'], self.data['Adj Close'], timeperiod=self.atr_long_period)

    def next(self):
        # Buy condition
        if self.rsi[-1] < self.buy_threshold and self.atr_short[-1] < self.atr_long[-1]:
            self.buy()
        # Sell condition
        elif self.position and (self.rsi[-1] > self.sell_threshold or self.atr_short[-1] > self.atr_long[-1]):
            self.position.close()
#########################################################################################################################################################
def risk_ind(data):
    """ a function to turn our HODL data into an indicator"""
    return data

####################################### Support & Resistance With Peak HODL Waves #######################################################################
class SupportAndResWithPeakHodl(Strategy):
    # Class variables for short-term (ST) and long-term (LT) periods
    ST = 10
    LT = 100

    def init(self):
        # Calculate highest highs and lowest lows over ST and LT periods
        self.highest_high_ST = self.I(talib.MAX, self.data.High, self.ST)
        self.highest_high_LT = self.I(talib.MAX, self.data.High, self.LT)
        self.lowest_low_ST = self.I(talib.MIN, self.data.Low, self.ST)
        # turn the HODL peak into a risk indicator
        self.riskOn=self.I(risk_ind, self.data["Peak"])
    
    def next(self):
        # Buy condition: Adj Close > highest high over ST AND LT periods
        if self.data["Adj Close"][-1] > self.highest_high_ST[-2] and self.data["Adj Close"][-1] > self.highest_high_LT[-2] and self.riskOn[-1] != 1:
            self.buy()

        # Sell condition: Adj Close < lowest low over ST OR peak detected
        if self.data["Adj Close"][-1] < self.lowest_low_ST[-2] or self.riskOn[-1] == 1:
            self.position.close()
####################################### Support & Resistance With Peak HODL Waves Optimized################################################################
class SupportAndResWithPeakHodl_opt(Strategy):
    # Class variables for short-term (ST) and long-term (LT) periods
    ST = 2
    LT = 150

    def init(self):
        # Calculate highest highs and lowest lows over ST and LT periods
        self.highest_high_ST = self.I(talib.MAX, self.data.High, self.ST)
        self.highest_high_LT = self.I(talib.MAX, self.data.High, self.LT)
        self.lowest_low_ST = self.I(talib.MIN, self.data.Low, self.ST)
        # turn the HODL peak into a risk indicator
        self.riskOn=self.I(risk_ind, self.data["Peak"])
    
    def next(self):
        # Buy condition: Adj Close > highest high over ST AND LT periods
        if self.data["Adj Close"][-1] > self.highest_high_ST[-2] and self.data["Adj Close"][-1] > self.highest_high_LT[-2] and self.riskOn[-1] != 1:
            self.buy()

        # Sell condition: Adj Close < lowest low over ST OR peak detected
        if self.data["Adj Close"][-1] < self.lowest_low_ST[-2] or self.riskOn[-1] == 1:
            self.position.close()

####################################### Support & Resistance With Peak HODL Waves #######################################################################
class SupportAndRes(Strategy):
    # Class variables for short-term (ST) and long-term (LT) periods
    ST = 10
    LT = 100

    def init(self):
        # Calculate highest highs and lowest lows over ST and LT periods
        self.highest_high_ST = self.I(talib.MAX, self.data.High, self.ST)
        self.highest_high_LT = self.I(talib.MAX, self.data.High, self.LT)
        self.lowest_low_ST = self.I(talib.MIN, self.data.Low, self.ST)
       
    def next(self):
        # Buy condition: Adj Close > highest high over ST AND LT periods
        if self.data["Adj Close"][-1] > self.highest_high_ST[-2] and self.data["Adj Close"][-1] > self.highest_high_LT[-2] :
            self.buy()

        # Sell condition: Adj Close < lowest low over ST OR peak detected
        if self.data["Adj Close"][-1] < self.lowest_low_ST[-2]:
            self.position.close()
############## test strategies ##########################################################################################################################
if __name__ == "__main__":
    df=pd.read_csv(r'BTC-USD.csv', index_col='Date',parse_dates=True)
    df=df.dropna()    
    df=df[df.index >= pd.to_datetime('2023-01-01')]
    print("----------MACD----------------")
    bt =Backtest(df, MACDStrategy, cash=100_000)
    stats = bt.run()
    print(stats)
    bt.plot(filename='test_plot.html')
    #
    print("----------rsi----------------")
    bt =Backtest(df, ATRRSIStrategy, cash=100_000)
    stats = bt.run()
    print(stats)
    bt.plot(filename='test_plot.html')
    #
    df=pd.read_csv(r'BTC-USD.csv', index_col='Date',parse_dates=True)
    df=df.dropna()    
    df_hodl=pd.read_csv(r'HODL.txt', index_col='Date',parse_dates=True)
    df=df.merge(df_hodl, how="left",left_index=True,right_index=True)
    df.Peak=df.Peak.fillna(0)
    print("----------S&R with HODL Peak----------------")
    bt =Backtest(df, SupportAndResWithPeakHodl, cash=100_000)
    stats = bt.run()
    print(stats)
    bt.plot(filename='test_plot.html')
    print("----------S&R ----------------")
    bt =Backtest(df, SupportAndRes, cash=100_000)
    stats = bt.run()
    print(stats)
    bt.plot(filename='test_plot.html')
    print("----------S&R with HODL Peak Optimized---------------")
    bt =Backtest(df, SupportAndResWithPeakHodl_opt, cash=100_000)
    stats = bt.run()
    print(stats)
    bt.plot(filename='test_plot.html')