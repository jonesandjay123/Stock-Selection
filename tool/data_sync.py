import glob
import os
from tool.helper import Helper
import pandas as pd
import datetime


class DataSync:
    def sync_hist_csv():
        print("====按鈕被點擊了====")
        # 取得當前路徑
        current_dir = os.getcwd()

        # 由於我們不確定 voo_stock_list.txt 檔案的確切位置，這裡我們假設它與當前 Python 檔案在同一個目錄下
        stock_list = Helper.load_stock_list('voo_stock_list.txt')[:80]

        # glob模塊可以找到符合特定規則的文件路徑名
        csv_files = glob.glob(os.path.join(
            current_dir, '**/*_top_N_result.csv'), recursive=True)

        # 對 csv_files 進行排序，使用 datetime.strptime 將檔案名稱轉換為 datetime 物件，再進行排序
        csv_files = sorted(csv_files, key=lambda x: datetime.datetime.strptime(
            os.path.basename(x).split('_')[0], '%Y-%m-%d'))

        sync_hist_path = os.path.join(current_dir, 'SyncHist.csv')

        # 刪除已存在的 SyncHist.csv
        if os.path.isfile(sync_hist_path):
            os.remove(sync_hist_path)

        # 創建SyncHist.csv檔案並寫入csv文件名稱
        rank_dict = {}
        score_dict = {}
        for file in csv_files:
            date = os.path.basename(file).split('_')[0]
            tmp_df = pd.read_csv(file)
            tmp_df['rank'] = tmp_df.index + 1
            tmp_df.set_index('symbol', inplace=True)
            rank_dict[date] = tmp_df.reindex(stock_list)['rank']
            score_dict[date] = tmp_df.reindex(stock_list)['score']

        rank_df = pd.concat(rank_dict, axis=1)
        score_df = pd.concat(score_dict, axis=1)
        final_df = pd.concat([score_df, rank_df], keys=[
                             'score', 'rank'], axis=1)

        final_df.to_csv(sync_hist_path)
        print("SyncHist.csv 已被創建，並且 csv 檔案的名稱已經寫入。")
