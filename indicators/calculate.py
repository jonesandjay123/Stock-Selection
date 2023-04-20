import pandas as pd
import numpy as np

class Calculator:
    def indicator(stock_data, indicator_func, periods, prefix):
        if stock_data.empty:
            return {}

        results = {}
        for period in periods:
            name = f'{prefix}_{period}'
            indicator = indicator_func(stock_data['adjClose'], timeperiod=period)
            results[name] = indicator.iloc[-1]

        return results
    
    def MACD(df, n_fast, n_slow, n_macd): # n_fast = 12, n_slow = 26, n_macd = 9
        EMAfast = df['Adj Close'].ewm(span=n_fast, min_periods=n_slow - 1).mean()
        EMAslow = df['Adj Close'].ewm(span=n_slow, min_periods=n_slow - 1).mean()
        MACD = EMAfast - EMAslow
        MACD_signal = MACD.ewm(span=n_macd, min_periods=n_macd-1).mean()
        df['MACD'] = MACD
        df['MACD_signal'] = MACD_signal
        df['MACD_hist'] = MACD - MACD_signal
        return df