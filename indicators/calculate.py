import pandas as pd
import numpy as np
import talib

class Calculator:
    def calculate_rsi(stock_data, rsi_periods):
        if stock_data.empty:
            return {}

        rsi_results = {}
        for period in rsi_periods:
            rsi_name = f'rsi{period}'
            rsi = talib.RSI(stock_data['adjClose'], timeperiod=period)
            rsi_results[rsi_name] = rsi.iloc[-1]

        return rsi_results
    
    def calculate_sma(stock_data, sma_periods):
        if stock_data.empty:
            return {}

        sma_results = {}
        for period in sma_periods:
            sma_name = f'sma{period}'
            sma = talib.SMA(stock_data['adjClose'], timeperiod=period)
            sma_results[sma_name] = sma.iloc[-1]

        return sma_results

    def calculate_ema(stock_data, ema_periods):
        if stock_data.empty:
            return {}

        ema_results = {}
        for period in ema_periods:
            ema_name = f'ema{period}'
            ema = talib.EMA(stock_data['adjClose'], timeperiod=period)
            ema_results[ema_name] = ema.iloc[-1]

        return ema_results
    
    def MACD(df, n_fast, n_slow, n_macd): # n_fast = 12, n_slow = 26, n_macd = 9
        EMAfast = df['Adj Close'].ewm(span=n_fast, min_periods=n_slow - 1).mean()
        EMAslow = df['Adj Close'].ewm(span=n_slow, min_periods=n_slow - 1).mean()
        MACD = EMAfast - EMAslow
        MACD_signal = MACD.ewm(span=n_macd, min_periods=n_macd-1).mean()
        df['MACD'] = MACD
        df['MACD_signal'] = MACD_signal
        df['MACD_hist'] = MACD - MACD_signal
        return df