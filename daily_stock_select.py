import requests
import json
from typing import List
from indicators.calculate import Calculator
from tqdm import tqdm  # 導入 tqdm

def read_access_token(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

API_KEY = read_access_token('access_token.txt')

def get_data(symbol: str) -> dict:
    interval = "60min"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize=compact&apikey={API_KEY}"
    print(f"url: {url}")
    r = requests.get(url)
    try:
        data = r.json()
        if f"Time Series ({interval})" not in data:
            print(f"Failed to get data for {symbol}: Time Series ({interval}) key not found")
            return None
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to get data for {symbol}: {e}")
        return None

def calculate_indicators(data: dict) -> dict:
    if data is None:
        return None
    # 計算技術指標（如均線、RSI 等），並返回指標數據
    indicators = {}
    rsi = Calculator.calculate_rsi(data)
    indicators["RSI"] = rsi
    return indicators

def select_stocks(stock_list: List[str]) -> List[dict]:
    selected_stocks = []
    
    for stock in tqdm(stock_list):  # 在迭代中使用 tqdm
        data = get_data(stock)
        indicators = calculate_indicators(data)
        
        if indicators is None:
            continue

        # 在這裡，您可以根據技術指標的結果判斷是否符合您的策略
        # 如果符合條件，則將股票添加到 selected_stocks 列表中

        # 這裡只是一個示例，我們假設所有股票都符合策略
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
    top_stocks = select_stocks(stock_list)
    
    results = []
    for idx, stock in enumerate(top_stocks):
        result = {
            "Ranking": idx + 1,
            "Symbol": stock["symbol"],
            "sell_price": stock["sell_price"],
            "buy_price": stock["buy_price"]
        }
        results.append(result)
    
    print(json.dumps(results, indent=2))