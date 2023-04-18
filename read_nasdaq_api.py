import nasdaqdatalink as ndl
import pandas as pd

# 設定你的API金鑰
def read_access_token(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

ndl.ApiConfig.api_key = API_KEY = read_access_token('access_token.txt')

# 使用快速方法獲取股票數據
data = ndl.get('WIKI/AAPL')

# 將數據轉換為pandas DataFrame
data_frame = pd.DataFrame(data)

# 查看前5行數據
print(data_frame.head())
