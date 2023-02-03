"""
Download data from https://tushare.pro
--------------------
Created by: Yanzhong Huang
Email: yanzhong.huang@outlook.com
"""

import pandas as pd
from utils import IndexData
from datetime import date
from dateutil.relativedelta import relativedelta


class Downloader:

    def __init__(self) -> None:
        self.index_data = IndexData()  # setting tushare object
        self.today = date.today()

    def download_stock_market_last_5_days(self, code: str, name: str):
        start_date = self.today - relativedelta(days=5)
        data = self.index_data.index_daily(ts_code=code,
                                           start_date=start_date.strftime(
                                               '%Y%m%d'),
                                           end_date=self.today.strftime('%Y%m%d'))[['trade_date', 'close', 'pct_chg']]
        data = self.set_trade_date_as_index(data)
        data = data.add_prefix(f'{name}_')
        return data

    def download_last_year_weekly(self, code: str, name: str):
        start_date = self.today - relativedelta(years=1)
        data =  self.index_data.index_weekly(ts_code=code,
                                           start_date=start_date.strftime('%Y%m%d'),
                                           end_date=self.today.strftime('%Y%m%d'))[['trade_date', 'close', 'pct_chg']]
        data = self.set_trade_date_as_index(data)
        data = data.add_prefix(f'{name}_')
        return data

    @staticmethod
    def set_trade_date_as_index(df):
        df.set_index('trade_date', inplace=True)
        df.index = pd.to_datetime(df.index).date
        df.sort_index(inplace=True)
        return df

    def loop_download(self, loop_dict: dict):
        weekly_data_list = []
        daily_data_list = []

        for name, code in loop_dict.items():
            weekly_data_list.append(self.download_last_year_weekly(code=code, name=name))
            daily_data_list.append(self.download_stock_market_last_5_days(code=code, name=name))
        
        return weekly_data_list, daily_data_list
