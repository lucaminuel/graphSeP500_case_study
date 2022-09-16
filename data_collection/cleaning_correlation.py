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
In this module we delete missing values from correlation matrix and rename
keys' dictionary as the referance year

"""
import time
import numpy as np


def clean_nan(data):
    '''

    Parameters
    ----------
    data : numpy.matrix
        correlation matrix.

    Returns
    -------
    data : numpy.matrix
        matri without NaN.

    '''
    column_drop = []
    for col in data.columns:
        if data[col].isnull().sum() == len(data[col]) -1:
            column_drop.append(col)
    data = data.drop(column_drop, axis = 1)
    row_drop = []
    for row in data.index:
        if data.loc[row].isnull().sum().sum() == len(data.columns):
            row_drop.append(row)
    data = data.drop(row_drop)
    return data


if __name__ == '__main__':
    start = time.time()
    # Load correlation dictionary
    corr = np.load('data\\correlation.npy',allow_pickle='TRUE').item()
    mykeys = [*corr]
    # remove nan from matrix
    for number in range (len(corr)) :
        year_corr = corr[mykeys[number]]
        year_corr = clean_nan(year_corr)
        corr[mykeys[number]] = year_corr
        print(f'Done {number +1 }/{len(corr) }')
    # array of year from 1962 to 2022
    name = range (1962, 1961 + len(corr) +1)
    # rename keys
    INDEX = 0
    for x in name:
        corr[x] = corr.pop(mykeys[INDEX])
        INDEX += 1
    #save dictionary
    np.save('data\\cleaned_corr.npy',corr)
    mins = (time.time()-start)//60
    sec = (time.time()-start) % 60
    print(f"Elapsed time: {mins} min {sec:.2f} sec\n")
