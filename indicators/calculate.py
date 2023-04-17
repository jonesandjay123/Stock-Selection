import pandas as pd
import numpy as np

class Calculator:
    def calculate_rsi(data: dict, period: int = 14) -> float:
        if "Time Series (60min)" not in data:
            print("Error: Time Series (60min) key not found in data")
            return None
        
        close_prices = [float(value["4. close"]) for value in data["Time Series (60min)"].values()]

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