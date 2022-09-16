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
In this module we compute yearly correlation matrix of our data from dataset.npy and
we save it in a dictionary
"""
import time
import collections
import numpy as np
import pandas as pd



if __name__ == '__main__':
    start = time.time()
    # Load dataset dictionary
    fps_hist_dict = np.load("data\\dataset.npy",allow_pickle='TRUE').item()
    # Take year of oldest firm in s&p500
    list_year = pd.unique(fps_hist_dict['PG'].resample('1Y').mean().index)
    # Create a correlation square matrix considering all given tickers
    list_corr = collections.defaultdict()
    for year in list_year:
        start2 = time.time()
        print(f"Starting {year}")
        corr_mtx = collections.defaultdict(dict)
        for kr, vr in fps_hist_dict.items():
            sr = fps_hist_dict[kr]['Close']
            sr = sr[sr.index < year]
            for kc, vc in fps_hist_dict.items():
                if kr == kc:
                    corr_mtx[kr][kc] = 1.0
                else:
                    sc = fps_hist_dict[kc]['Close']
                    # Compute the correlation
                    corr_mtx[kr][kc] = round(sc.corr(sr),2)
        corr_mtx = pd.DataFrame(corr_mtx)
        list_corr[year] = corr_mtx
        mins = (time.time()-start2)//60
        sec = (time.time()-start2) % 60
        print(f"Elapsed time: {mins} min {sec:.2f} sec\n")
    np.save('data\\correlation.npy', list_corr)
    hours = (time.time()-start)//(60*60) % 60
    mins = ((time.time()-start)//60)% 60
    sec = (time.time()-start) % 60
    print(f"Elapsed time:{hours} hour {mins} min {sec:.2f} sec\n")
