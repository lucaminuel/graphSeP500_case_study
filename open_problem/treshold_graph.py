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
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from data_collection.graph_building import  creating_graph
from data_collection.graph_splitting import create_neg_network
from data_collection.label_graph import label_graph



def draw_graph(G, title):
    """
    This function make and save plot of a graph

    Args:
        G (networkx.classes.graph.Graph): Graph
        name (string): name of the title
        map_color = if use cmap
    """    
    pos = nx.spring_layout(G, seed=7)
    ec = nx.draw_networkx_edges(G, pos, width = 1, edge_color='blue')
    nc = nx.draw_networkx_nodes(G, pos, node_color='red',
                                edgecolors = 'black',
                                label=False, node_size=10)
    plt.axis('off')
    plt.title(f"{title}")

if __name__ == '__main__':
    start = time.time()
    dataset = pd.read_csv('data\\stock_code.csv')
    dataset = dataset[['Symbol','Sector']]
    list_graph = np.load('data\\list_graph.npy',allow_pickle='TRUE').item()
    mykeys = [*list_graph]
    # Treshold d <1
    TRESHOLD = -1 # -1 due to our function definition
    list_graph_tresh  = collections.defaultdict()
    for number in range (len(list_graph)) :
        graph_tmp = list_graph[mykeys[number]]
        graph = create_neg_network(graph_tmp, treshold = TRESHOLD)
        list_graph_tresh[mykeys[number]] = graph
        print(f'Done {number +1 }/{len(list_graph_tresh)}')
    list_graph_tresh = label_graph(list_graph_tresh, dataset)
    #saving new graph dictionary
    np.save('data\\list_graph_tresh.npy',list_graph_tresh)
    #Make plot
    fig = plt.subplots(figsize = (10,5))
    draw_graph(list_graph_tresh[0], 'Normal period (23-07-1985)')
    plt.savefig("plots\\tresh_normal.pdf", format="pdf", bbox_inches="tight")
    plt.show()
    draw_graph(list_graph_tresh[1], 'Bubble period (08-01-2007)')
    plt.savefig("plots\\tresh_bubble.pdf", format="pdf", bbox_inches="tight")
    plt.show()
    draw_graph(list_graph_tresh[2], 'Crash period (17-06-2010)')
    plt.savefig("plots\\tresh_crash.pdf", format="pdf", bbox_inches="tight")
    plt.show()
    draw_graph(list_graph_tresh[3], 'Covid Period (2020-04-01)')
    plt.savefig("plots\\tresh_covid.pdf", format="pdf", bbox_inches="tight")
    plt.show()
    mins = (time.time()-start)//60
    sec = (time.time()-start) % 60
    print(f"Elapsed time: {mins} min {sec:.2f} sec\n")
    