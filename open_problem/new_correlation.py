# -*- coding: utf-8 -*-
# Copyright 2022 Manuel Luci, Alessandro Seccarelli, Ayushi Ayushi
#
# This file is part of  sna-project-2022_luci_seccarelli_ayushi
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
"""
In this module we collect in a dictionary the daily record 194 stock of S&P 500 useful for open question, we evaluate correlation
metrix (as distance) in 4 different time periods and save them in a dictionary
"""


import time
import collections
import numpy as np
import pandas as pd
import datapackage
import yfinance as yf
import seaborn as sb
import matplotlib.pyplot as plt



def distance_correlation(x):
    """
    Evaluate distance from correlation value

    Args:
        x: array, dataframe

    Returns:
        array, dataframe: distance
    """        

    distance = np.sqrt(2*(1-x))
    return distance


def daily_return_log(data, end, number: int = 40):
    """
    Evaluate the log daily return of the stock at "number" days before the end one.

    Args:
        data (array): close value of stock
        end (datetime64): date of the last day
        number (int, optional): how many days evaluate log daily return. Defaults to 40.

    Returns:
        _type_: _description_
    """    """"""
    final_return = []
    for index in range (data.index.get_loc(end)-40,data.index.get_loc(end)):
        x = np.log(data[index +1]) - np.log(data[index])
        final_return.append(x)
    return final_return



if __name__ == '__main__':
    start = time.time()
    STOCK = pd.read_csv('data\\stock_code.csv',index_col= False)
    ticker = np.array(STOCK['Symbol'])
    fps_hist_dict = collections.defaultdict()
    dataset_len = len(ticker)
    # Collect the data from yahoofinance
    if ticker is not None:
            for code in ticker:
                print(f'Start {code}')
                print(f"[{list(ticker).index(code)+ 1}/{dataset_len}] Fetching historic data for {code}")
                fp = yf.Ticker(code)
                fp_hist = fp.history(period='max', auto_adjust = True, interval='1d')
                # auto_adjust = True : Close -> Adj. Close
                if fp_hist.empty:
                    print(f"- WARN: No history data is available for {code} > It will be skipped")
                else:
                    fps_hist_dict[code] = fp_hist
    else:
        raise Exception('No data has been loaded')
    np.save("data\\new_correlation.npy", fps_hist_dict)
    #Evaluate correlation matrix
    DATE = ('1985-07-23', '2007-01-08', '2010-06-17', '2020-04-01')
    corr_dict = collections.defaultdict(dict)
    for date in DATE:
        corr_mtx = collections.defaultdict(dict)
        for kr, vr in fps_hist_dict.items():
            print(f'Start {kr}')
            try:
                corr_mtx[kr] = daily_return_log(fps_hist_dict[kr]['Close'],date)
            except Exception:
                print(f'{kr} has no data')
            pass
        corr_mtx = pd.DataFrame(corr_mtx)
        corr_mtx = corr_mtx.corr()
        #Evaluate distance matrix from correlation matrix
        dist_corr = corr_mtx.apply(distance_correlation)
        corr_dict[DATE.index(date)] = dist_corr
    # Save dictionary of our historic data

    np.save("data\\new_correlation.npy", corr_dict)
    # Make plots
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1,len(corr_dict),figsize = (25,9))
    ax1= sb.heatmap(corr_dict[0], cbar=False,ax=ax1)
    ax2= sb.heatmap(corr_dict[1], cbar=False,ax=ax2)
    ax3= sb.heatmap(corr_dict[2],ax=ax3)
    ax4= sb.heatmap(corr_dict[3])
    ax1.set_title(' Heatmap Normal period (23-07-1985)')
    ax2.set_title('Heatmap Bubble period (08-01-2007)')
    ax3.set_title('Heatmap Crash period (17-06-2010)')
    ax4.set_title('Heatmap Covid Period (2020-04-01)')
    plt.savefig("plots\\heatmap.pdf", format="pdf", bbox_inches="tight")
    plt.show()
    mins = (time.time()-start)//60
    sec = (time.time()-start) % 60
    print(f"Elapsed time: {mins} min {sec:.2f} sec\n")
