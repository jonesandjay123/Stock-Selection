import json
import datetime
import pandas as pd
import nasdaqdatalink as ndl

N = 15  # 宣告N的值

# https://github.com/Nasdaq/data-link-python
def get_top_N_stocks(N):
    # 設定日期範圍（過去一年）
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)

    # 可根據需要自定義股票清單
    stock_list = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'TSLA', 'IBM', 'NVDA', 'NFLX', 'BA']

    stock_results = []

    for stock_symbol in stock_list:
        # 獲取股票歷史數據
        stock_data = ndl.get(f'WIKI/{stock_symbol}', start_date=start_date, end_date=end_date)
        stock_df = pd.DataFrame(stock_data)
        # 計算平均收盤價
        average_close = stock_df['Close'].mean()

        # 計算平均交易量
        average_volume = stock_df['Volume'].mean()

        # 計算買入價與賣出價
        buy_price = average_close * 0.9
        sell_price = average_close * 1.1

        # 將結果加入stock_results
        stock_results.append({'symbol': stock_symbol, 'average_close': average_close, 'average_volume': average_volume, 'buy_price': buy_price, 'sell_price': sell_price})

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
