import requests
import pandas as pd

# 設定你的API金鑰
def read_access_token(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

API_KEY = read_access_token('access_token.txt')

# 使用Tiingo API獲取股票數據
def get_stock_data(ticker):
    headers = {
        'Content-Type': 'application/json'
    }
    url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices?token={API_KEY}'
    request_response = requests.get(url, headers=headers)
    return request_response.json()

data = get_stock_data('AAPL')

# 將數據轉換為pandas DataFrame
data_frame = pd.DataFrame(data)

# 查看前5行數據
print(data_frame.head())
