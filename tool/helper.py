import datetime
import json
import os
import shutil

class Helper:
    @staticmethod
    def read_access_token(file_name):
        with open(file_name, 'r') as file:
            return file.read().strip()
        
    @staticmethod
    def load_stock_list(file_path):
        with open(file_path, 'r') as f:
            stock_list = json.load(f)
        return stock_list

    @staticmethod
    def trading_days_to_actual_days(trading_days):
        weeks = trading_days / 5
        actual_days = int(weeks * 7)
        return actual_days
    
    @staticmethod
    def filter_periods(periods, max_days):
        return [period for period in periods if period <= max_days]
    
    @staticmethod
    def clean_old_csv_folders():
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        for folder in os.listdir():
            if folder.endswith('_csv') and not folder.startswith(current_date):
                shutil.rmtree(folder)

    @staticmethod
    def prepare_cache_folder():
        cache_folder_name = f"{datetime.date.today()}_csv"
        if not os.path.exists(cache_folder_name):
            os.makedirs(cache_folder_name)
        return cache_folder_name