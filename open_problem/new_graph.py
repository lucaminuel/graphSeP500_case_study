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
In this module we extract graphs from new correlation matrix
"""
import time
import collections
import numpy as np
import networkx as nx
import sys
import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from data_collection.graph_building import  creating_graph
from data_collection.graph_splitting import create_neg_network
from data_collection.label_graph import label_graph



if __name__ == '__main__':
    start = time.time()
    dataset = pd.read_csv('data\\stock_code.csv')
    dataset = dataset[['Symbol','Sector']]
    # Load cleaned correlation dictionary
    corr = np.load('data\\new_correlation.npy',allow_pickle='TRUE').item()
    mykeys = [*corr]
    list_graph = collections.defaultdict()
    # create a dictionary of graph
    for number in range (len(corr)) :
        data_year = corr[mykeys[number]]
        G = creating_graph(data_year)
        list_graph[mykeys[number]] = G
        print(f'Done {number +1 }/{len(corr) }')
    list_graph = label_graph(list_graph, dataset)
    np.save('data\\list_graph.npy',list_graph)
    mins = (time.time()-start)//60
    sec = (time.time()-start) % 60
    print(f"Elapsed time: {mins} min {sec:.2f} sec\n")
