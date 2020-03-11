# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import scipy
import scipy.io
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

#%% Read data.

ain = pd.read_csv('precincts_stats_by_ethnicity.csv')

bout = ain.groupby(['county','name'],as_index = False)['caucus_turnout_2008'].sum()

cout = ain[ain.ethnicity.isin(['White'])]
dout = cout.drop(['ethnicity', 'registered', 'total_registered', 'total_caucus_turnout_2016', 'total_caucus_turnout_2008', 'ethnicity_registered_pct', 'ethnicity_caucus_turnout_2008_pct'], axis=1)
dout = dout.set_index(['county', 'district'])

dout.to_csv('cleaned.csv')

#%% Add identifier column

df = dout.copy()
df = df.reset_index()

df['county'] = df['county'].str.strip()

df['COMBNAME'] = df.county.map(str) + "_" + df.short_precinct_name
df['COMBNAME'] = df.COMBNAME.str.upper()
df = df.set_index(['COMBNAME'])

#%% Combine with VAN_Pct_ID

df_van = pd.read_csv('ia_precinct_shapefile_matchv2.csv')
df_van['County'] = df_van['County'].str.strip()

df_van['COMBNAME'] = df_van.County.map(str) + "_" + df_van.Short_Precinct_Name
df_van['COMBNAME'] = df_van.COMBNAME.str.upper()
df_van = df_van.set_index(['COMBNAME'])

df_merged = df_van.merge(df, on='COMBNAME', how='outer')

#%% Combine with COMMITGOALS

df_commits = pd.read_csv('./COMMITGOALS/0125.csv')
#df_commits['County'] = df_commits['County'].str.strip()
#
#df_commits['COMBNAME'] = df_commits.County.map(str) + "_" + df_commits.Precinct
#df_commits['COMBNAME'] = df_commits.COMBNAME.str.upper()

#df_updated = df_merged.merge(df_commits, on='COMBNAME', how='outer')
df_updated = pd.merge(df_merged, df_commits, left_on='VAN_Precinct_Code', right_on='Precinct ID')

#%% Export to CSV with GeoJSON

df_updated.rename(columns=lambda x: x.strip(), inplace=True) #strip trailing whitespace from headers

colstomap = ['VAN_Precinct_Code', 
             'county', 
             'name', 
             'population', 
             'congressional_district',
             'short_precinct_name',
             'Combined',
             'Delegates',
             'Commit Goal - 298',
             'Commits',
             'PTG',
             'Difference to Delegate Threshold',
             'Precinct Captains',
             'geojson']
df_tomap = df_updated[colstomap].copy()

df_tomap['PTG'] = df_tomap['PTG'].str.rstrip('%').astype('float')  # make percentage column float

df_tomap.rename(columns={"Commit Goal - 298": "Goal", "PTG":"Progress (%)", "Difference to Delegate Threshold": "Remaining"}, inplace=True)
df_tomap = df_tomap.set_index('VAN_Precinct_Code')

df_tomap.to_csv('./For_Kepler/Precinct_Progress.csv')  #export for Kepler.gl
df_tomap['Commits'] = df_tomap['Commits'].astype(float)

#%% Calculate progess statistics

#df_tomap['congressional_district'] = df_tomap['congressional_district'].astype(np.int64)

cdcoms = df_tomap.groupby(['congressional_district']).sum()['Commits']
cdgoals = df_tomap.groupby(['congressional_district']).sum()['Goal']
cdptg = 100* cdcoms / cdgoals
ax = cdptg.plot.bar(rot=0)
ax.set_ylabel('Commits as % of viability')
