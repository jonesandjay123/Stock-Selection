import json
import datetime
import pandas as pd
import requests

N = 3  # 宣告N的值
interval_days = 5  # 宣告日期範圍

def read_access_token(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

API_KEY = read_access_token('access_token.txt')

def get_stock_data(stock_symbol, start_date, end_date):
    headers = {'Content-Type': 'application/json'}
    request_url = f"https://api.tiingo.com/tiingo/daily/{stock_symbol}/prices?startDate={start_date}&endDate={end_date}&token={API_KEY}"
    response = requests.get(request_url, headers=headers)
    return response.json()

def get_top_N_stocks(N):
    # 設定日期範圍（過去interval_days範圍內）
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=interval_days)

    # 可根據需要自定義股票清單
    stock_list = ['AAPL', 'MSFT', 'AMZN', 'META', 'TSLA', 'NVDA']

    stock_results = []

    for stock_symbol in stock_list:
        try:
            # 獲取股票歷史數據
            stock_data = get_stock_data(stock_symbol, start_date, end_date)
            stock_df = pd.DataFrame(stock_data)

            # 計算平均收盤價
            average_close = stock_df['adjClose'].mean()

            # 計算平均交易量
            average_volume = stock_df['adjVolume'].mean()

            # 計算買入價與賣出價
            buy_price = average_close * 0.9
            sell_price = average_close * 1.1

            # 將結果加入stock_results
            stock_results.append({'symbol': stock_symbol, 'average_close': average_close, 'average_volume': average_volume, 'buy_price': buy_price, 'sell_price': sell_price})
        
        except Exception as e:
            print(f"Error processing {stock_symbol}: {e}. Skipping this stock.")
            continue

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
