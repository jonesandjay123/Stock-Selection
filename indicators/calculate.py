import pandas as pd
import numpy as np


class Calculator:
    @staticmethod
    def indicator(stock_data, indicator_func, periods, prefix):
        if stock_data.empty:
            return {}

        results = {}
        for period in periods:
            name = f'{prefix}_{period}'
            indicator = indicator_func(
                stock_data['adjClose'], timeperiod=period)
            results[name] = indicator

        return results

    @staticmethod
    def MACD(df, n_fast, n_slow, n_macd):  # n_fast = 12, n_slow = 26, n_macd = 9
        EMAfast = df['Adj Close'].ewm(
            span=n_fast, min_periods=n_slow - 1).mean()
        EMAslow = df['Adj Close'].ewm(
            span=n_slow, min_periods=n_slow - 1).mean()
        MACD = EMAfast - EMAslow
        MACD_signal = MACD.ewm(span=n_macd, min_periods=n_macd-1).mean()
        df['MACD'] = MACD
        df['MACD_signal'] = MACD_signal
        df['MACD_hist'] = MACD - MACD_signal
        return df

    @staticmethod
    def calculate_stock_scores(stock_data_list, stock_order):
        stock_scores = []

        for stock_data in stock_data_list:
            score = 0
            indicators = stock_data['indicators']

            # 計算近期（5天）和長期（20天）平均交易量
            volume_5 = indicators['volume_5'][-1]
            volume_20 = indicators['volume_20'][-1]
            volume_ratio = volume_5 / volume_20

            # 根據近期與長期平均交易量的比例，更新評分
            if volume_ratio > 1.5:
                score += 1

            # 檢查交易量突破
            recent_volume = stock_data['latest_date_data']['volume']
            if recent_volume > volume_20 * 1.5:
                score += 1

            # RSI
            rsi_5 = indicators['rsi_5'][-1]
            if rsi_5 < 30:
                score += 1
            elif rsi_5 > 70:
                score -= 1

            # Bollinger Bands
            close_price = stock_data['latest_date_data']['adjClose']
            bollinger_upper = indicators['bollinger_upper'][-1]
            bollinger_lower = indicators['bollinger_lower'][-1]
            if close_price > bollinger_upper:
                score -= 1
            elif close_price < bollinger_lower:
                score += 1

            # Moving Average Strategy
            sma_5 = indicators['sma_5'][-1]
            sma_20 = indicators['sma_20'][-1]
            if sma_5 > sma_20:
                score += 1
            elif sma_5 < sma_20:
                score -= 1

            # MACD
            macd = indicators['macd'][-1]
            macdsignal = indicators['macdsignal'][-1]
            if macd > macdsignal:
                score += 1
            elif macd < macdsignal:
                score -= 1

            stock_scores.append({
                'symbol': stock_data['symbol'],
                'score': score
            })

        # 根據分數排序，分數相同的話，根據 stock_order 的順序排序
        stock_scores.sort(key=lambda x: (
            x['score'], stock_order[x['symbol']]), reverse=True)

        return stock_scores
