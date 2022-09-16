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
In this module we add sector of stocks as label of graphs' nodes
"""
import time
import collections
import numpy as np
import pandas as pd

def label_graph(list_tot, data):
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
    list_label = collections.defaultdict()
    mykeys = [*list_tot]
    for number in range (len(list_tot)) :
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
        test = list_tot[mykeys[number]]
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
        list_label[mykeys[number]] = test
        print(f'Done {number +1 }/{len(list_tot) }')
    return list_label




if __name__ == '__main__':
    start = time.time()
    dataset = pd.read_csv('data\\dataset_infromation.csv')
    list_neg_graph = np.load('graph\\list_neg_graph.npy',allow_pickle='TRUE').item()
    list_pos_graph = np.load('graph\\list_pos_graph.npy',allow_pickle='TRUE').item()
    list_tot_graph = np.load('graph\\list_graph.npy',allow_pickle='TRUE').item()
    dataset = dataset[['Symbol','Sector']]
    # Add label to total graph
    list_tot_label = label_graph(list_tot_graph, dataset)
    print('\nDone total \n')
    # Add label to positive graph
    list_pos_label = label_graph(list_pos_graph, dataset)
    print('\nDone positive \n')
    # Add label to negative graph
    list_neg_label = label_graph(list_neg_graph, dataset)
    print('\nDone negative \n')
    np.save('graph\\list_graph_label.npy', list_tot_label)
    np.save('graph\\list_pos_graph_label.npy', list_pos_label)
    np.save('graph\\list_neg_graph_label.npy', list_neg_label)
    mins = (time.time()-start)//60
    sec = (time.time()-start) % 60
    print(f"Elapsed time: {mins} min {sec:.2f} sec\n")
