import pandas as pd
import numpy as np

class Calculator:
    def calculate_rsi(data: dict, period: int = 14) -> float:
        # 從Alpha Vantage提供的數據中提取收盤價
        close_prices = [float(value["4. close"]) for value in data["Time Series (Daily)"].values()]

        # 計算價格變動
        deltas = np.diff(close_prices)

        # 將變動分為增長和下跌兩個序列
        gains = deltas.copy()
        gains[gains < 0] = 0
        losses = -deltas.copy()
        losses[losses < 0] = 0

        # 計算平均收益和平均損失
        avg_gain = np.sum(gains[-period:]) / period
        avg_loss = np.sum(losses[-period:]) / period

        # 計算RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi