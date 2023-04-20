import pandas as pd
import numpy as np

class Calculator:
    def calculate_rsi(stock_data, periods):
        if not stock_data:
            print("Error: Stock data is empty")
            return None

        close_prices = [float(row['adjClose']) for row in stock_data]
        deltas = np.diff(close_prices)

        gains = deltas.copy()
        gains[gains < 0] = 0
        losses = -deltas.copy()
        losses[losses < 0] = 0

        rsi_results = {}
        for period in periods:
            avg_gain = np.sum(gains[-period:]) / period
            avg_loss = np.sum(losses[-period:]) / period

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            rsi_results[f"RSI_{period}"] = rsi

        return rsi_results
    
    def calculate_sma(stock_data, periods):
        if not stock_data:
            print("Error: Stock data is empty")
            return None

        close_prices = pd.Series([float(row['adjClose']) for row in stock_data])
        sma_results = {}
        for period in periods:
            sma = close_prices.rolling(window=period).mean().iloc[-1]
            sma_results[f"SMA_{period}"] = sma

        return sma_results
    
    def calculate_ema(stock_data, periods, source_data=None):
        if not stock_data:
            print("Error: Stock data is empty")
            return None

        # 使用傳入的 source_data 或者股票收盤價
        if source_data is None:
            data_series = pd.Series([float(row['adjClose']) for row in stock_data])
        else:
            data_series = pd.Series(source_data)

        ema_results = {}
        for period in periods:
            alpha = 2 / (period + 1)
            ema = data_series.ewm(alpha=alpha, adjust=False).mean().iloc[-1]
            ema_results[f"EMA_{period}"] = ema

        return ema_results
    
    def calculate_macd(stock_data):
        if not stock_data:
            print("Error: Stock data is empty")
            return None
        
        ema_12 = Calculator.calculate_ema(stock_data, [12])
        ema_26 = Calculator.calculate_ema(stock_data, [26])
        macd_line = ema_12['EMA_12'] - ema_26['EMA_26']
        signal_line = Calculator.calculate_ema(stock_data, [9], macd_line)
        histogram = macd_line - signal_line['EMA_9']
        
        return {
            'MACD_Line': macd_line,
            'MACD_Signal': signal_line['EMA_9'],
            'MACD_Histogram': histogram
        }