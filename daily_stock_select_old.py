import requests
import json
from typing import List
from indicators.calculate import Calculator
from tqdm import tqdm

# https://docs.data.nasdaq.com/docs/in-depth-usage
def read_access_token(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

API_KEY = read_access_token('access_token.txt')

# 修改 get_data 函數以使用 Nasdaq Data Link API
def get_data(symbol: str) -> dict:
    start_date = "2021-01-01"
    end_date = "2021-12-31"
    url = f"https://data.nasdaq.com/api/v3/datatables/WIKI/PRICES?ticker={symbol}&date.gte={start_date}&date.lte={end_date}&api_key={API_KEY}"
    print(url)
    r = requests.get(url)
    try:
        data = r.json()
        if "datatable" not in data:
            print(f"Failed to get data for {symbol}: datatable key not found")
            return None
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to get data for {symbol}: {e}")
        return None

def calculate_indicators(data: dict) -> dict:
    if data is None:
        return None

    # 使用新的資料格式提取收盤價
    close_prices = [row[11] for row in data["datatable"]["data"]]

    # 在這裡計算您需要的技術指標
    # ...

    indicators = {
        # "RSI": rsi,
        # "SMA": sma,
        # ...
    }
    return indicators

def select_stocks(stock_list: List[str]) -> List[dict]:
    selected_stocks = []

    for stock in tqdm(stock_list):
        data = get_data(stock)
        indicators = calculate_indicators(data)

        if indicators is None:
            continue

        # 為了簡單起見，這裡只是一個示例，我們假設所有股票都符合策略
        selected_stocks.append({
            "symbol": stock,
            "sell_price": 100,
            "buy_price": 90
        })

    # 根據您的策略對 selected_stocks 進行排序，然後返回前 15 名
    top_stocks = selected_stocks[:15]

    return top_stocks

if __name__ == "__main__":
    with open('voo_stock_list.txt', 'r') as f:
        stock_list = json.load(f)
    stock_list = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'NVDA']
    top_stocks = select_stocks(stock_list)

    # 根據新的資料格式修改結果處理部分
    results = []
    for idx, stock in enumerate(top_stocks):
        result = {
            "Ranking": idx + 1,
            "Symbol": stock["symbol"],
            "Price": {"sell_price": stock["sell_price"], "buy_price": stock["buy_price"]}
        }
        results.append(result)

    print(json.dumps(results, indent=2))