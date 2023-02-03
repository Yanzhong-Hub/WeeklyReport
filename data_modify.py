"""
modify downloaded data
--------------------
Created by: Yanzhong Huang
Email: yanzhong.huang@outlook.com
"""

import datetime
import pandas as pd


def find_year_start(weekly_data):
    newest_year = weekly_data.index[-1].year
    last_year = newest_year - 1
    
    year_end = datetime.date(last_year, 12, 31)
    year_end_2 = datetime.date(last_year, 12, 30)
    year_end_3 = datetime.date(last_year, 12, 29)
    if year_end in weekly_data.index:
        return year_end
    if year_end_2 in weekly_data.index:
        return year_end_2
    if year_end_3 in weekly_data.index:
        return year_end_3


def concat_data(data_list: list):
    return pd.concat(data_list, axis=1, join='inner')


def run_modify(weekly_data_list: list, daily_data_list: list):
    # 合并指数列表数据
    weekly_data = concat_data(weekly_data_list)
    this_week_data = concat_data(daily_data_list)

    # modify data
    weekly_data, this_week_data = if_weekly_data_newest(weekly_data, this_week_data)
    this_week_data = slice_last_week_data(weekly_data, this_week_data)

    # select data
    year_start = find_year_start(weekly_data=weekly_data)
    this_year_data = weekly_data.loc[year_start:, :]

    # result
    last_year_close = select_close(weekly_data)
    this_year_close = select_close(this_year_data)
    this_week_pct_chg = this_week_daily_return(this_week_data=this_week_data)
    
    return last_year_close, this_year_close, this_week_pct_chg
    


def if_weekly_data_newest(weekly_data, this_week_data):
    """周频数据更新速度较慢，日频数据更新较快，如周频数据未更新，用最新的日频数据做替代"""
    weekly_last = weekly_data.index[-1]
    newest = this_week_data.index[-1]

    if weekly_last != newest:
        weekly_data.loc[newest] = this_week_data.loc[newest]

    return weekly_data, this_week_data


def slice_last_week_data(weekly_data, this_week_data):
    """日频数据默认为最近5个交易日，当上周时间不足5日时，对日频数据进行切割"""

    # 判断周频数据是否更新
    weekly_last = weekly_data.index[-1]
    newest = this_week_data.index[-1]

    if weekly_last != newest:
        weekly_data.loc[newest] = this_week_data.loc[newest]

    # 对日频数据进行更改
    last_friday = weekly_data.index[-2]
    return this_week_data.loc[last_friday:, :]


def select_close(weekly_data):
    selection_list = []
    for _ in weekly_data.columns:
        if 'close' in _ :
            selection_list.append(_)

    return weekly_data[selection_list].copy()


def this_week_daily_return(this_week_data):
    
    selection_list = []
    for _ in this_week_data.columns:
        if 'pct' in _ :
            selection_list.append(_)

    return this_week_data[selection_list].copy()/100