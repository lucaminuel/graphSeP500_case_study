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
In this module we split graphs into positive and negative correlated (given treshold)
"""
import time
import collections
import numpy as np


def create_pos_network(graph, treshold = 0.8):
    '''

    Parameters
    ----------
    graph : networkx.classes.graph.Graph
        graph.
    treshold : float, optional
        treshold. The default is 0.8

    Returns
    -------
    h_graph : networkx.classes.graph.Graph
        splitted graph.

    '''
    h_graph = graph.copy()
    # Checks all the edges and removes some based on corr_direction
    for stock1, stock2, weight  in list(graph.edges(graph, data = True)):
        for weight in weight.values():
            # if we only want to see the positive correlations
            # then we delete the edges with weight smaller than trashold
            if weight <= treshold :
                h_graph.remove_edge(stock1, stock2)
    return h_graph

def create_neg_network(graph, treshold = 0.5):
    '''

    Parameters
    ----------
    graph : networkx.classes.graph.Graph
        graph.
    treshold : float, optional
        treshold. The default is 0.5

    Returns
    -------
    h_graph : networkx.classes.graph.Graph
        splitted graph.

    '''
    h_graph = graph.copy()
    # Checks all the edges and removes some based on corr_direction
    for stock1, stock2, weight  in list(graph.edges(graph, data = True)):
        for weight in weight.values():
            # if we only want to see the negative correlations we
            # then we delete the edges with weight greater than - treshold
            if weight >= -treshold:
                h_graph.remove_edge(stock1, stock2)
    return h_graph

if __name__ == '__main__':
    start = time.time()
    list_graph = np.load('graph\\list_graph.npy',allow_pickle='TRUE').item()
    list_pos_graph = collections.defaultdict()
    list_neg_graph  = collections.defaultdict()
    mykeys = [*list_graph]
    TRESHOLDPOS = 0.8
    TRESHOLDNEG = 0.5
    for number in range (len(list_graph)) :
        graph_tmp = list_graph[mykeys[number]]
        positive = create_pos_network(graph_tmp, treshold = TRESHOLDPOS)
        negative = create_neg_network(graph_tmp, treshold = TRESHOLDNEG)
        list_pos_graph[mykeys[number]] = positive
        list_neg_graph[mykeys[number]] = negative
        print(f'Done {number +1 }/{len(list_graph) }')
    np.save('graph\\list_pos_graph.npy',list_pos_graph)
    np.save('graph\\list_neg_graph.npy',list_neg_graph)
    mins = (time.time()-start)//60
    sec = (time.time()-start) % 60
    print(f"Elapsed time: {mins} min {sec:.2f} sec\n")
