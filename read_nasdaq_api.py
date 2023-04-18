import requests

# https://github.com/Nasdaq/data-link-python
def read_access_token(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

# 替換 YOUR_API_KEY 為您的 API 密鑰
api_key = read_access_token('access_token.txt')

# 選擇股票代碼和數據集代碼
stock_symbol = "AAPL"
dataset_code = "WIKI"

# 創建 API 請求 URL
url = f"https://data.nasdaq.com/api/v3/datatables/{dataset_code}/PRICES?ticker={stock_symbol}&api_key={api_key}"
# print(url)

# 發送請求並獲取 JSON 數據
response = requests.get(url)
data = response.json()

# 檢查並輸出數據
if "datatable" in data and "data" in data["datatable"]:
    stock_data = data["datatable"]["data"]
    for daily_data in stock_data:
        print(daily_data)
else:
    print("Error fetching data.")