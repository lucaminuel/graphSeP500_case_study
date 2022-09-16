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
In this module we collect in a dictionary the daily record of s&p500 stocks until July 2022 and
save it in a .npy file.
"""
import time
import collections
import numpy as np
import pandas as pd
import datapackage
import yfinance as yf



if __name__ == '__main__':
    start = time.time()
    DATA_URL = r"https://datahub.io/core/s-and-p-500-companies/datapackage.json"
    # To load Data Package into storage
    package = datapackage.Package(DATA_URL)
    # To load only tabular data
    DATA = None
    resources = package.resources
    for resource in resources:
        if resource.tabular:
            dataset = pd.read_csv(resource.descriptor['path'])
    dataset = dataset.sort_values('Symbol').reset_index(drop=True)
    dataset.to_csv('data\\dataset_infromation.csv', index=False)
    # Load historic data for all stocks via yfinance
    fps_hist_dict = collections.defaultdict()
    dataset_len = len(dataset)
    if dataset is not None:
        for index, row in dataset.iterrows():
            ticker = row['Symbol']
            print(f"[{(index + 1)}/{dataset_len}] Fetching historic data for {ticker}")
            fp = yf.Ticker(ticker)
            fp_hist = fp.history(period='max', auto_adjust = True, interval='1d') 
            # auto_adjust = True : Close -> Adj. Close
            if fp_hist.empty:
                print(f"- WARN: No history data is available for {ticker} > It will be skipped")
            else:
                fps_hist_dict[ticker] = fp_hist
    else:
        raise Exception('No data has been loaded')
    # Save dictionary of our historic data
    np.save("data\\dataset.npy", fps_hist_dict)
    mins = (time.time()-start)//60
    sec = (time.time()-start) % 60
    print(f"Elapsed time: {mins} min {sec:.2f} sec\n")
