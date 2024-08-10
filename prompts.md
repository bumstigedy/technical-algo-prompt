A few notes: I had to force it write the code using Adj Close instead of close  sometimes it uses self.sell() instead of self.position.close() so I had to specify that in the prompt.  The first time it never closed the position I told this to chatGPT and it revised the code correctly.   

MACD prompt:

I have a python data frame with "Open", "High", "Low", and "Adj Close" data.  The close price is ["Adj Close"] not Close 
write python code using the following libraries: """backtesting.py and ta-lib.py"""  to create a backtest strategy to buy when the following conditions are met: """MACD crosses above the signal line and the 20 day ema is above the 100 day ema"""  and to close the position when the following conditions are met: """MACD crosses below the signal line or the 20 day ema crosses below the 100 day ema"""  make the MACD fast, slow, and signal periods class variables and set them to the default values

RSI Prompt:

I have a python data frame with "Open", "High", "Low", and "Adj Close" data.  
write python code using the following libraries: """backtesting.py and ta-lib.py"""  to create a backtest strategy to buy when the following conditions are met: """RSI is below buy_threshold AND the 14 day ATR is below the 100 day ATR"""  and to close the position using self.positoin.close () when the following conditions are met: """RSI is above sell_threshold OR the 14 day ATR is above the 100 day ATR  make the atr time periods class variables  set buy_threshold to 30 and sell_threshold to 70"""

Support & Resistance with HODL Peak prompt:  this one was a bit hard for chatGPT :(   It got close and was a good start/base for coding the strategy, but it needed a bit of additional effort to make it work.  

I have a python data frame with "Open", "High", "Low", and "Adj Close" data.  The close price is ["Adj Close"] not Close.  I have another python dataframe called df_hodl containing a column with the date and a column called peak that indicates a peak if a 1 is present.    
write python code using the following libraries: """backtesting.py and ta-lib.py"""  import talib as talib to create an indicator from df_hodl which will be included in the plot and to create a backtest strategy to buy when the following conditions are met: """ Adj Close is greater than highest high over the short term period called ST AND the Adj Close is greater than the highest high over the long term period called LT """  and to close the position when the following conditions are met: """Adj Close is lower than the lowest low over the short term period called ST OR df_hodl indicates a peak based on a 1 in the hodl column"""  make the LT and ST periods class variables and set them to 10 and 100  Use ta-lib min and max to determine the highest high and lowest lows over the periods and use self.position.close to close the positions
call the strategy support_and_res_with_peak_hodl
us the package ta-lib not ta
integrate df_hodl with df by joining on the date
