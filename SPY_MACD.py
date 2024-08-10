from backtesting import Backtest, Strategy
import pandas as pd
import talib
from backtesting.lib import crossover

#
df=pd.read_csv(r'/home/sanjay/venv/SPY.csv', index_col='Date',parse_dates=True)
df=df.dropna()
print(df.tail())
#

def risk_ind(data):
    return data


class MACD_Kiss(Strategy):
    short_window=12
    long_window=26
    signal_window=9

    def init(self):
        
        self.macd, self.signal, self.hist = talib.MACD(
            self.data.Close,
            fastperiod=self.short_window,
            slowperiod=self.long_window,
            signalperiod=self.signal_window
        )
        self.ema100=self.I(talib.EMA, self.data["Adj Close"],100)
        self.ema20=self.I(talib.EMA, self.data["Adj Close"],20)

        # Save the MACD and Signal line as class variables
        self.macd_ind = self.I(risk_ind, self.macd, plot=False)
        self.signal_ind = self.I(risk_ind,self.signal, plot=False)
        self.hist_ind = self.I(risk_ind, self.hist)
        
    def next(self):
        if (crossover(self.signal_ind, self.macd_ind) and self.ema20 > self.ema100 ):
            self.buy()
        elif (crossover(self.macd_ind,self.signal_ind) or self.ema20 < self.ema100 ):
            self.position.close()

class MAVG(Strategy):
    
    def init(self):
        
        self.ema100=self.I(talib.EMA, self.data["Adj Close"],100)
        self.ema20=self.I(talib.EMA, self.data["Adj Close"],20)
    
    def next(self):
        if crossover(self.ema20, self.ema100):
            self.buy()
        elif crossover(self.ema100,self.ema20):
            self.position.close()

class BB(Strategy):
    
    def init(self):
        
        self.ema100=self.I(talib.EMA, self.data["Adj Close"],100, plot=False)
        self.ema20=self.I(talib.EMA, self.data["Adj Close"],20, plot=False)
        self.upper_band, self.middle_band, self.lower_band = self.I(talib.BBANDS,self.data["Adj Close"], 20 )

        self.upper_ind = self.I(risk_ind,self.upper_band, plot=False)
        self.middle_ind = self.I(risk_ind,self.middle_band, plot=False)
        self.lower_ind = self.I(risk_ind,self.lower_band, plot=False)
        

    def next(self):
        if crossover(self.ema20, self.ema100):
            self.buy()
        elif crossover(self.ema100,self.ema20):
            self.position.close()

class oscillator(Strategy):
    
    def init(self):
       self.stochRSI = self.I(talib.RSI,self.data["Adj Close"],14)     
       self.RSI_smoothed=self.I(talib.DEMA, self.stochRSI,14)                            
    def next(self):
        if self.RSI_smoothed <40:
            self.buy()
        elif self.RSI_smoothed>70:
            self.position.close()




# print("MAVG----------------")
# bt =Backtest(df, MAVG, cash=100_000)
# stats = bt.run()
# print(stats)
# bt.plot(filename='backtest_plot.html')

# print("Bollinger Band----------------")
# bt =Backtest(df, BB, cash=100_000)
# stats = bt.run()
# print(stats)
# bt.plot(filename='backtest_plot.html')

# print("Oscillator----------------")
# bt =Backtest(df, oscillator, cash=100_000)
# stats = bt.run()
# print(stats)
# bt.plot(filename='backtest_plot.html')


print("KISS wiht MACD----------------")
bt =Backtest(df, MACD_Kiss, cash=100_000)
stats = bt.run()
print(stats)
bt.plot(filename='backtest_plot.html')
