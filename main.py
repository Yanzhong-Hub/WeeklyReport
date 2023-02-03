"""
市场周报输出
--------------------
Created by: Yanzhong Huang
Email: yanzhong.huang@outlook.com
"""

import pandas as pd
from data_modify import run_modify
from download import Downloader
from result import result_all
from plot_result import plot_save

def main():

    stock_index_dict = index_dict = {'上证指数': '000001.SH',
                                     # '深证成指': '399001.SZ',
                                     '创业板指': '399006.SZ',
                                     # '上证50': '000016.SH',
                                     '沪深300': '000300.SH',
                                     '中证500': '000905.SH',
                                     '中证1000': '000852.SH'}

    # create instances
    downloader = Downloader()

    # downloading data
    weekly_list, daily_list = downloader.loop_download(loop_dict=stock_index_dict)
    
    # modify data
    last_year_close, this_year_close, this_week_pct = run_modify(weekly_data_list=weekly_list, daily_data_list=daily_list)
    
    # result
    results  = result_all(this_year_close, this_week_pct)
    print('股票周度表格')
    print(results[0])
    print('上证指数日度涨跌幅')
    print(results[1])

    # save table
    writer = pd.ExcelWriter('results/结果.xlsx', engine='openpyxl')
    results[0].to_excel(writer, sheet_name='股票市场')
    results[1].to_excel(writer, sheet_name='上证指数日度涨跌幅')
    writer.close()
    
    print('绘图中..')
    plot_save(last_year_close)
    print('运行结束')
    # plot

if __name__ == '__main__':
    main()
