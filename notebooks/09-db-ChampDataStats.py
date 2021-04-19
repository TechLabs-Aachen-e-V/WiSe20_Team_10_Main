# -*- coding: utf-8 -*-
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

# +
#Before running this file, make sure this Jupyter notebook is in the following folder of datadragon of that patch

# dragontail-10.25.1/10.25.1/data/en_GB/champion
# -

import pandas as pd
import numpy as np
import json
import glob

# +
#For One Champion (Pantheon)

with open('../data/raw/Pantheon.json') as json_file:
    champ = json.load(json_file)
    

champname = champ['data']['Pantheon']['name']
xyz = {'name':champname}


y = champ['data']['Pantheon']['info']

z = champ['data']['Pantheon']['stats']


somestring = ['mp', 'mpperlevel','mpregen', 'mpregenperlevel','crit','critperlevel']
for i in somestring:
    z.pop(i)

xyz.update(y)

xyz.update(z)

dataa = pd.DataFrame.from_dict(xyz,orient='index').T
df = pd.DataFrame(columns=dataa.columns)
# -

df

filenames = glob.glob('*.json')

# +
#For all champions

for i in filenames:
    with open(i) as json_file:
        champ = json.load(json_file)
        name = i.split('.json')[0]
    champname = champ['data'][name]['name']
    xyz = {'name':champname}
    y = champ['data'][name]['info']
    z = champ['data'][name]['stats']
    somestring = ['mp', 'mpperlevel','mpregen', 'mpregenperlevel','crit','critperlevel']
    for i in somestring:
        z.pop(i)
    xyz.update(y)
    xyz.update(z)
    dat = pd.DataFrame.from_dict(xyz,orient='index').T
    df = pd.concat([df,dat])
# -

df.head()

df.reset_index(inplace=True)

df.drop('index',axis=1,inplace=True)

df.head()

df['Tags']=np.nan

df

df.to_csv('../data/processed/ChampionAttributes.csv',index=False)

# +
#In order to get the tags for our champions (tags here describe the functionality/type of that particular champ)
#I used the following website: https://leagueoflegends.fandom.com/wiki/List_of_champions
#Rather than importing the data and working on it, manually entering the roles seemed easier
#So I opened the csv file and added every entry of tag manually
#For some champions, secondary tag was also given, but that didnt seem that relevant.
#So basically its one tag per champion
# -







# +
#After doing that, I saved the file under the name  'ChampionAttributes-Tags.csv'
# -

df_tags = pd.read_csv('../data/processed/ChampionAttributes-Tags.csv')

df_tags.columns

df_tags

df_tags.drop(['attack','defense','magic','difficulty'],axis=1,inplace=True)

df_tags.to_csv('../data/processed/ChampionStats.csv',index=False)


