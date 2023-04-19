import json
import datetime
import pandas as pd
import requests
from indicators.calculate import Calculator


# https://api.tiingo.com/documentation/end-of-day
N = 3  # 挑選前N名最直得投資的股票
rsi_periods = [5, 10, 14]  # 宣告RSI計算期限種類
sma_periods = [5, 10, 20, 50, 100]  # 宣告SMA計算期限種類
ema_periods = [5, 10, 20, 50, 100]  # 宣告EMA計算期限種類

def trading_days_to_actual_days(trading_days):
    weeks = trading_days / 5
    actual_days = int(weeks * 7)
    return actual_days

data_interval_days = trading_days_to_actual_days(200)   # 搜尋資料的天數範圍

def filter_periods(periods, max_days):
    return [period for period in periods if period <= max_days]

# 過濾大於data_interval_days的rsi_periods和sma_periods
rsi_periods = filter_periods(rsi_periods, data_interval_days)
sma_periods = filter_periods(sma_periods, data_interval_days)
ema_periods = filter_periods(ema_periods, data_interval_days)

def read_access_token(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

API_KEY = read_access_token('access_token.txt')

def get_stock_data(stock_symbol, start_date, end_date):
    headers = {'Content-Type': 'application/json'}
    request_url = f"https://api.tiingo.com/tiingo/daily/{stock_symbol}/prices?startDate={start_date}&endDate={end_date}&token={API_KEY}"
    response = requests.get(request_url, headers=headers)
    stock_data = response.json()

    indicators = calculate_indicators(stock_data)

    # 獲取前一個交易日的數據
    latest_date_data = stock_data[-1]

    return stock_data, indicators, latest_date_data

def calculate_indicators(data):
    if data is None:
        return None

    # 在這裡計算您需要的技術指標
    rsi = Calculator.calculate_rsi(data, rsi_periods)
    sma = Calculator.calculate_sma(data, sma_periods)
    ema = Calculator.calculate_ema(data, ema_periods)
    macd = Calculator.calculate_macd(data)

    indicators = {
        **rsi,
        **sma,
        **ema,
        # 'macd': macd,
    }
    return indicators

def get_top_N_stocks(N):
    # 設定日期範圍（過去一年）
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(data_interval_days)

    # 可根據需要自定義股票清單
    stock_list = ['AAPL', 'META', 'TSLA']
    # stock_list = ['AAPL', 'ADBE', 'AMC', 'AMZN', 'META', 'MSFT', 'NVDA', 'TSLA']
    # 讀取整個voo_stock_list.txt中的200支股票
    # with open('voo_stock_list.txt', 'r') as f:
    #     stock_list = json.load(f)

    stock_results = []

    for stock_symbol in stock_list:
        # 獲取股票歷史數據
        stock_data, indicators, latest_date_data = get_stock_data(stock_symbol, start_date, end_date)
        stock_df = pd.DataFrame(stock_data)
        
        # 計算平均收盤價
        average_close = stock_df['adjClose'].mean()

        # 計算平均交易量
        average_volume = stock_df['adjVolume'].mean()

        # 計算買入價與賣出價
        recommand_buy_price = average_close * 0.9
        recommand_sell_price = average_close * 1.1

        # 將結果加入stock_results
        stock_results.append({
            'symbol': stock_symbol,
            'latest_date_data': latest_date_data,
            'average_close': average_close,
            'average_volume': average_volume,
            'recommand_buy_price': recommand_buy_price,
            'recommand_sell_price': recommand_sell_price,
            'indicators': indicators,
        })

    # 根據平均交易量降序排序，取前N名
    top_N_stocks = sorted(stock_results, key=lambda x: x['average_volume'], reverse=True)[:N]

    return top_N_stocks

def main():
    top_N_stocks = get_top_N_stocks(N)

    # 將結果轉為JSON格式
    top_N_stocks_json = json.dumps(top_N_stocks, indent=2)

    # 輸出結果
    print(top_N_stocks_json)

if __name__ == "__main__":
    main()
