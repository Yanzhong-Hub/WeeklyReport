"""
输出结果
--------------------
Created by: Yanzhong Huang
Email: yanzhong.huang@outlook.com
"""

import numpy as np
import pandas as pd

def result_all(this_year_close, this_week_pct):
    result = output_table(this_year_close)
    result_this_week = output_this_week(this_week_pct=this_week_pct)

    # change percentage
    result['本周涨跌幅'] = result['本周涨跌幅'].map('{:.2%}'.format)
    result['今年以来涨跌幅'] = result['今年以来涨跌幅'].map('{:.2%}'.format)
    result['今年以来最大回撤'] = result['今年以来最大回撤'].map('{:.2%}'.format)
    result_this_week = result_this_week.map('{:.2%}'.format)
    return (result, result_this_week)


def output_table(this_year_close):
    latest_close = this_year_close.iloc[-1, :]
    this_week_return = this_year_close.iloc[-1, :] / this_year_close.iloc[-2, :] - 1
    this_year_return = this_year_close.iloc[-1, :] / this_year_close.iloc[0, :] - 1
    this_year_max_draw_back = max_draw_back(this_year_close)

    newest_week_rank = this_week_rank(this_year_close)
    count_positive = count_positive_week(this_year_close)
    data = pd.concat([latest_close, this_week_return, this_year_return,
                     this_year_max_draw_back, newest_week_rank, count_positive], axis=1)
    data.columns = ['本周收盘价', '本周涨跌幅', '今年以来涨跌幅',
                    '今年以来最大回撤', '年初至今周排名', '上涨周数(包括0)', '下跌周数']
    data.index = [_[:-6] for _ in data.index]
    return data
    

def output_this_week(this_week_pct):
    data = this_week_pct['上证指数_pct_chg']
    data.name = '上证指数日涨跌幅'
    return data


def max_draw_back(data):
    """回撤率"""
    data_drop_na = data.dropna().copy()
    draw_back_list = (data_drop_na - np.maximum.accumulate(data_drop_na)
                      ) / np.maximum.accumulate(data_drop_na)

    return draw_back_list.min()


def this_week_rank(this_year_close):
    drifts = this_year_close / this_year_close.shift(1) - 1
    ranked_drifts = drifts.rank(ascending=False).dropna()
    
    last_week_rank = ranked_drifts.iloc[-1, :]
    all_week_count = ranked_drifts.shape[0]

    output = [str(_) + '/' + str(all_week_count) for _ in last_week_rank]
    output = pd.Series(output, name='年初至今周排名', index=last_week_rank.index)

    return output


def count_positive_week(this_year_close):
    weekly_drifts = this_year_close / this_year_close.shift(1) - 1
    weekly_drifts.dropna(inplace=True)
    weekly_drifts[weekly_drifts >= 0] = 1
    weekly_drifts[weekly_drifts < 0] = None

    output = pd.concat([weekly_drifts.count(), weekly_drifts.shape[0] - weekly_drifts.count()], axis=1)
    output.index = weekly_drifts.columns
    output.columns = ['上涨周数(包括0)', '下跌周数']
    return output
        