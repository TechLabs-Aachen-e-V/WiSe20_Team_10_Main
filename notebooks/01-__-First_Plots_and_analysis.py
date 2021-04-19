# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
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
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline


df = pd.read_csv('../data/processed/ChampionStats.csv')

df.head()

plt.hist(df['Totalwinrate'])

plt.plot(df['Totalwinrate'],df['TotalPlayed'],'*')



plt.plot(df['Redwinrate']-df['Bluewinrate'],'*',color='green')

df[df['Totalwinrate']>0.55]

df[(df['Redwinrate']-df['Bluewinrate']).abs()>0.05]

len(df[(df['Redwinrate']-df['Bluewinrate']).abs()>0.05])

df[df['TotalPlayed']-df['#Role1']-4*df['#Role2']>0]


