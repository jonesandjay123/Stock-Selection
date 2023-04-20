import pandas as pd
import numpy as np
import talib

class Calculator:
    def indicator(stock_data, indicator_type, periods):
        if stock_data.empty:
            return {}

        indicator_function_map = {
            'rsi': talib.RSI,
            'sma': talib.SMA,
            'ema': talib.EMA,
        }

        if indicator_type not in indicator_function_map:
            raise ValueError(f"Invalid indicator type: {indicator_type}")

        indicator_function = indicator_function_map[indicator_type]
        indicator_results = {}

        for period in periods:
            indicator_name = f'{indicator_type}{period}'
            indicator = indicator_function(stock_data['adjClose'], timeperiod=period)
            indicator_results[indicator_name] = indicator.iloc[-1]

        return indicator_results
    
    def MACD(df, n_fast, n_slow, n_macd): # n_fast = 12, n_slow = 26, n_macd = 9
        EMAfast = df['Adj Close'].ewm(span=n_fast, min_periods=n_slow - 1).mean()
        EMAslow = df['Adj Close'].ewm(span=n_slow, min_periods=n_slow - 1).mean()
        MACD = EMAfast - EMAslow
        MACD_signal = MACD.ewm(span=n_macd, min_periods=n_macd-1).mean()
        df['MACD'] = MACD
        df['MACD_signal'] = MACD_signal
        df['MACD_hist'] = MACD - MACD_signal
        return df