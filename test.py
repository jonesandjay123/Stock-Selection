import nasdaqdatalink as ndl
import pandas as pd

# 設定你的API金鑰
ndl.ApiConfig.api_key = "你的API金鑰"

# 使用快速方法獲取股票數據
data = ndl.get('WIKI/AAPL')

# 將數據轉換為pandas DataFrame
data_frame = pd.DataFrame(data)

# 查看前5行數據
print(data_frame.head())
