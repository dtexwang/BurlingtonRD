# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import scipy
import scipy.io
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

#%% Import Data

aa = pd.read_csv('iowa_results.csv')
bb = aa[aa.Precinct == 'Total']
bb.to_csv('iowa_bycounty.csv')

#%% Rank Yang

colstomap = ['County', 
             'Biden SDE', 
             'Buttigieg SDE', 
             'Klobuchar SDE', 
             'Sanders SDE',
             'Steyer SDE',
             'Warren SDE',
             'Yang SDE',
             'Uncommitted SDE']
cc = bb[colstomap].copy()
dd = cc.reset_index()               # renumber
ee = dd.drop(columns = ['index'], axis=1)     # drop old index column

nrows = ee.shape[0]     # number of rows (Counties)

for ii in range(nrows):
    
    cc1 = ee.loc[ii]
    cc2 = pd.DataFrame(cc1.tolist()[1:9], index=['Biden', 'Buttigieg', 'Klobuchar', 'Sanders', 'Steyer', 'Warren', 'Yang', 'Uncommitted'], columns=['SDE'])
    
    ccr = cc2.rank(method='min', ascending = False).astype(int)
    
    pos = ccr.at['Yang', 'SDE']     # get Yang's position in county
    
    ee.loc[ii, 'Position'] = pos
    
#%% Sort by Yang's position in county

ff = ee.sort_values('Position')

ff['Yang (%)'] = ff.iloc[:, 7] / ff.iloc[:, 1:9].sum(axis=1) *100

gg = ff.sort_values(['Yang (%)'], ascending=False)

colstomap = ['County', 
             'Yang SDE',
             'Position',
             'Yang (%)']
hh = gg[colstomap].copy()   # Final Result DF
hh.to_csv('Final_Results_Yang_Position.csv') 