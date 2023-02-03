"""
绘制各指数近一年走势图
--------------------
Created by: Yanzhong Huang
Email: yanzhong.huang@outlook.com
"""

import matplotlib.pyplot as plt

from utils.matplotlib_ch_font import matplot_ch_font

matplot_ch_font()

def plot_save(last_year_close):

    for column in last_year_close.columns:
        fig, ax = plt.subplots()
        ax.plot(last_year_close[column])
        ax.set_title(f'{column[:-6]}近一年走势')
        # ax = last_year_close[column].plot(title=f'{column[:-6]}近一年走势')
        fig.savefig(f'results/{column[:-6]}.png')
        

