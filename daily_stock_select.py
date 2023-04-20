import json
import datetime
import os
import pandas as pd
import requests
import talib
from indicators.calculate import Calculator
from tool.helper import Helper  
from tqdm import tqdm

def get_stock_data(stock_symbol, start_date, end_date, cache_folder_name):
    cache_file_path = os.path.join(cache_folder_name, f"{stock_symbol}.csv")

    if os.path.exists(cache_file_path):
        stock_data = pd.read_csv(cache_file_path).to_dict('records')
    else:
        headers = {'Content-Type': 'application/json'}
        request_url = f"https://api.tiingo.com/tiingo/daily/{stock_symbol}/prices?startDate={start_date}&endDate={end_date}&token={API_KEY}"
        response = requests.get(request_url, headers=headers)
        stock_data = response.json()
        stock_df = pd.DataFrame(stock_data)
        stock_df.to_csv(cache_file_path, index=False)

    indicators = calculate_indicators(stock_data)
    latest_date_data = stock_data[-1] # 獲取前一個交易日的數據
    return stock_data, indicators, latest_date_data

def calculate_indicators(stock_data):
    if stock_data is None:
        return None

    # 將股票數據轉換為 Pandas DataFrame
    stock_data = pd.DataFrame(stock_data)

    # Calculate indicators
    rsi_data = {}
    for period in rsi_periods:
        rsi_data[f"rsi_{period}"] = talib.RSI(stock_data["adjClose"], timeperiod=period)

    sma_data = {}
    for period in sma_periods:
        sma_data[f"sma_{period}"] = talib.SMA(stock_data["adjClose"], timeperiod=period)

    ema_data = {}
    for period in ema_periods:
        ema_data[f"ema_{period}"] = talib.EMA(stock_data["adjClose"], timeperiod=period)

    macd, macdsignal, macdhist = talib.MACD(stock_data["adjClose"], fastperiod=12, slowperiod=26, signalperiod=9)

    bb_upper, bb_middle, bb_lower = talib.BBANDS(stock_data["adjClose"], timeperiod=20)

    obv = talib.OBV(stock_data["adjClose"], stock_data["adjVolume"])

    indicators = {
        **rsi_data,
        **sma_data,
        **ema_data,
        "macd": macd,
        "macdsignal": macdsignal,
        "macdhist": macdhist,
        "bollinger_upper": bb_upper,
        "bollinger_middle": bb_middle,
        "bollinger_lower": bb_lower,
        "obv": obv
    }

    return indicators

def get_top_N_stocks(stock_list, N, indicator_display_amount, cache_folder_name):
    end_date = datetime.date.today() # 獲取當前日期
    start_date = end_date - datetime.timedelta(data_interval_days) # 獲取前data_interval_days天的日期

    stock_results = []

    for stock_symbol in tqdm(stock_list, desc="Processing stocks"):
        # 獲取股票歷史數據
        stock_data, indicators, latest_date_data = get_stock_data(stock_symbol, start_date, end_date, cache_folder_name)
        stock_df = pd.DataFrame(stock_data)
        
        average_close = stock_df['adjClose'].mean() # 計算平均收盤價
        average_volume = stock_df['adjVolume'].mean() # 計算平均交易量

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
            'indicators': {k: v[-indicator_display_amount:].tolist() if isinstance(v, pd.Series) else v for k, v in indicators.items()}, # 只顯示最近indicator_display_amount天的數據
        })

    # 根據平均交易量降序排序，取前N名
    top_N_stocks = sorted(stock_results, key=lambda x: x['average_volume'], reverse=True)[:N]

    return top_N_stocks

def main():
    Helper.clean_old_csv_folders() # 清理舊的CSV資料夾
    cache_folder_name = Helper.prepare_cache_folder() # 準備緩存資料夾
    top_N_stocks = get_top_N_stocks(stock_list, N, indicator_display_amount, cache_folder_name) # 取得前N名股票
    top_N_stocks_json = json.dumps(top_N_stocks, indent=2) # 將結果轉為JSON格式

    # 輸出結果
    print(top_N_stocks_json)

if __name__ == "__main__":
    # https://api.tiingo.com/documentation/end-of-day
    API_KEY = Helper.read_access_token('access_token.txt')
    # 可根據需要自定義股票清單
    # stock_list = Helper.load_stock_list('voo_stock_list.txt') # 讀取整個voo_stock_list.txt中的200支股票
    # stock_list = ['AAPL', 'ADBE', 'AMC', 'AMZN', 'META', 'MSFT', 'NVDA', 'TSLA']
    stock_list = ['AAPL', 'META', 'TSLA']

    N = 3  # 挑選前N名最直得投資的股票
    indicator_display_amount = 5  # 顯示最近幾天的指標數據
    rsi_periods = [5, 10, 14]  # 宣告RSI計算期限種類
    sma_periods = [5, 10, 20, 50, 100]  # 宣告SMA計算期限種類
    ema_periods = [5, 10, 20, 50, 100]  # 宣告EMA計算期限種類
    data_interval_days = Helper.trading_days_to_actual_days(200)   # 搜尋資料的天數範圍
    rsi_periods = Helper.filter_periods(rsi_periods, data_interval_days)
    sma_periods = Helper.filter_periods(sma_periods, data_interval_days)
    ema_periods = Helper.filter_periods(ema_periods, data_interval_days)
    main()
