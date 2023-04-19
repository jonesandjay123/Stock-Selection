import pandas as pd
import numpy as np

class Calculator:
    def calculate_rsi(stock_data, period):
        if not stock_data:
            print("Error: Stock data is empty")
            return None

        close_prices = [float(row['adjClose']) for row in stock_data]

        deltas = np.diff(close_prices)

        gains = deltas.copy()
        gains[gains < 0] = 0
        losses = -deltas.copy()
        losses[losses < 0] = 0

        avg_gain = np.sum(gains[-period:]) / period
        avg_loss = np.sum(losses[-period:]) / period

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi