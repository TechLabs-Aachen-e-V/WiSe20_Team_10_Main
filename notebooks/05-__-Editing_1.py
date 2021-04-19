# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import numpy as np
import pandas as pd

df = pd.read_csv('../data/raw/games.csv')

df.info()

champions = df['team_1'][0]
champions = champions.split(',')

champions[0]

df['BTop'] = df['winner']
df['BJng'] = df['winner']
df['BMid'] = df['winner']
df['BAdc'] = df['winner']
df['BSup'] = df['winner']


df.to_csv('Editing.csv',index=False)

for i in range(32955):
    champions = df['team_1'][i]
    champions = champions.split(',')
    df['BTop'][i] = champions[0]
    df['BJng'][i] = champions[1]
    df['BMid'][i] = champions[2]
    df['BAdc'][i] = champions[3]
    df['BSup'][i] = champions[4]

df['RTop'] = df['winner']
df['RJng'] = df['winner']
df['RMid'] = df['winner']
df['RAdc'] = df['winner']
df['RSup'] = df['winner']


df

for i in range(32955):
    champions = df['team_2'][i]
    champions = champions.split(',')
    df['RTop'][i] = champions[0]
    df['RJng'][i] = champions[1]
    df['RMid'][i] = champions[2]
    df['RAdc'][i] = champions[3]
    df['RSup'][i] = champions[4]

df

df['Time'] = df['timestamp'] +' '+ df['duration']

df['Time'].nunique()

abc.loc[0]['duration'] = '26m 00s'

abc.loc[0]['duration'] = '26m 18s'

df.drop_duplicates(subset='Time',keep='first',inplace=True)

df

df.drop(['team_1','team_2'],axis=1,inplace=True)

df.drop(['timestamp','duration'],axis=1,inplace=True)

df['Winner']=df['winner']

df






