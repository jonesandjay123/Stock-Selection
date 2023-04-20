import datetime
import os
import shutil

class Helper:
    def read_access_token(file_name):
        with open(file_name, 'r') as file:
            return file.read().strip()

    def trading_days_to_actual_days(trading_days):
        weeks = trading_days / 5
        actual_days = int(weeks * 7)
        return actual_days
    
    def filter_periods(periods, max_days):
        return [period for period in periods if period <= max_days]
    
    def clean_old_csv_folders():
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        for folder in os.listdir():
            if folder.endswith('_csv') and not folder.startswith(current_date):
                shutil.rmtree(folder)

    def prepare_cache_folder():
        cache_folder_name = f"{datetime.date.today()}_csv"
        if not os.path.exists(cache_folder_name):
            os.makedirs(cache_folder_name)
        return cache_folder_name