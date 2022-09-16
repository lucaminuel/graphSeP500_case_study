# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 09:49:09 2022

@author: manue
"""

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
In this module we compute correlation matrix of our stocks and save it as file csv
"""
import time
import collections
import numpy as np
import pandas as pd
import networkx as nx
from graph_splitting import create_neg_network, create_pos_network


def label_graph_tot(graph, data):
    '''

    Parameters
    ----------
    list_tot : dictionary
        dictionary of graph.
    data: pandas.DataFrame
        dataframe contaning infomation about stock sector

    Returns
    -------
    list_tot : dictionary
        dictionary graph label.

    '''
    list_health_care = []
    list_industrial = []
    list_consumer_discretionary = []
    list_information_technology = []
    list_consumer_staples = []
    list_utilities = []
    list_financials = []
    list_materials = []
    list_real_estate = []
    list_energy = []
    list_communication_services =[]
    test = graph
    list_name = list(test.nodes)
    mydata = data.loc[data['Symbol'].isin(list_name)]
    for name in list_name:
        condiction = (data['Symbol'] == name)
        x_tmp = mydata[condiction]['Sector']
        if (x_tmp == 'Utilities').bool() == True:
            list_utilities.append(name)
        elif (x_tmp == 'Industrials').bool() == True:
            list_industrial.append(name)
        elif (x_tmp == 'Energy').bool() == True:
            list_energy.append(name)
        elif (x_tmp == 'Communication Services').bool() == True:
            list_communication_services.append(name)
        elif (x_tmp == 'Information Technology').bool() == True:
            list_information_technology.append(name)
        elif (x_tmp == 'Materials').bool() == True:
            list_materials.append(name)
        elif (x_tmp == 'Health Care').bool() == True:
            list_health_care.append(name)
        elif (x_tmp == 'Consumer Discretionary').bool() == True:
            list_consumer_discretionary.append(name)
        elif (x_tmp == 'Financials').bool() == True:
            list_financials.append(name)
        elif (x_tmp == 'Real Estate').bool() == True:
            list_real_estate.append(name)
        else:
            list_consumer_staples.append(name)
    for x_tmp in list_health_care:
        test.remove_node
        test.add_node(x_tmp, label='Health Care')
    for x_tmp in list_industrial:
        test.remove_node
        test.add_node(x_tmp, label='Industrial')
    for x_tmp in list_consumer_discretionary:
        test.remove_node
        test.add_node(x_tmp, label='Consumer Discretionary')
    for x_tmp in list_information_technology:
        test.remove_node
        test.add_node(x_tmp, label='Information Technology')
    for x_tmp in list_consumer_staples:
        test.remove_node
        test.add_node(x_tmp, label='Consumer Staples')
    for x_tmp in list_utilities:
        test.remove_node
        test.add_node(x_tmp, label='Utilities')
    for x_tmp in list_financials:
        test.remove_node
        test.add_node(x_tmp, label='Financials')
    for x_tmp in list_materials:
        test.remove_node
        test.add_node(x_tmp, label='Materials')
    for x_tmp in list_real_estate:
        test.remove_node
        test.add_node(x_tmp, label='Real Estate')
    for x_tmp in list_energy:
        test.remove_node
        test.add_node(x_tmp, label='Energy')
    for x_tmp in list_communication_services:
        test.remove_node
        test.add_node(x_tmp, label='Communication_services')
    graph_final = test
    return graph_final


if __name__ == '__main__':
    start = time.time()
    # Load dataset dictionary
    fps_hist_dict = np.load("data\\dataset.npy",allow_pickle='TRUE').item()
    # Take year of oldest firm in s&p500
    list_year = pd.unique(fps_hist_dict['PG'].resample('1Y').mean().index)
    # Create a correlation square matrix considering all given tickers
    print('Evaluate correlation matrix...')
    corr_mtx = collections.defaultdict(dict)
    for kr, vr in fps_hist_dict.items():
        sr = fps_hist_dict[kr]['Close']
        for kc, vc in fps_hist_dict.items():
            if kr == kc:
                corr_mtx[kr][kc] = 1.0
            else:
                sc = fps_hist_dict[kc]['Close']
                # Compute the correlation
                corr_mtx[kr][kc] = round(sc.corr(sr),2)
    corr_mtx = pd.DataFrame(corr_mtx)
    data = np.asmatrix(corr_mtx)
    stocks = corr_mtx.index
    print('Creating graph...')
    graph = nx.from_numpy_matrix(data)
    graph = nx.relabel_nodes(graph,lambda x: stocks[x])
    print('Graph created!\nSplitting in positive and negative')
    positive = create_pos_network(graph)
    negative = create_neg_network(graph)
    data = pd.read_csv('data\\dataset_infromation.csv')
    print('Adding label...')
    pos_label = label_graph_tot(positive, data)
    neg_label = label_graph_tot(negative, data)
    print('Saving data...')
    nx.write_gpickle(pos_label,'graph\\pos_graph_tot.gpickle')
    nx.write_gpickle(neg_label,'graph\\neg_graph_tot.gpickle')
    hours = (time.time()-start)//(60*60) % 60
    mins = ((time.time()-start)//60)% 60
    sec = (time.time()-start) % 60
    print(f"Elapsed time:{hours} hour {mins} min {sec:.2f} sec\n")