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

# # To analyze champion data in more detail across roles
#
#
#
#

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

df = pd.read_csv('../data/processed/ChampionStats.csv')

df.head()

df.drop(['Role2','#Role2'],axis=1,inplace=True)

df.head()

df.describe()

sns.distplot(df['Totalwinrate'])

# #### We can see from the above plot that most of the winrate distribution is between 47% to 52%
#

df['#Role1'].min()

df[df['#Role1']==80]

# #### From this we can observe that a minimum a champion was played in its primary role was 80 games (and we can consider this a good enough data size)

sns.jointplot(x='Totalwinrate',y='#Role1',data=df,kind='hex')

# #### Since we have considered only champions in the primary roles, it has to be noted that there wasnt any niche picks
#
# #### Also we can conclude that the champions which were played the most (or OP champs as we call it), had winrates slightly better than chance
#
# #### We can also derive the fact that high variance in winrates across the two ends of the spectrum is due to insufficient data pool wrt to the other champions

# ### Now lets have a look at which champions were OP AND popular
#

df[(df['Totalwinrate']>0.49) & (df['#Role1']>1000)]


len(df[(df['Totalwinrate']>0.49) & (df['#Role1']>1000)])

# ## There are a total of 40 popular and OP champs, lets have a closer look at them
#
# #### Why only these 40 you might wonder, mainly because these 40 champions had more impact on the game (both in winrate and choice of selection) and one of our hypothesis is that these champions will have more say in how our model is being built

popchamp = df[(df['Totalwinrate']>0.49) & (df['#Role1']>1000)]
popchamp = popchamp.copy()


fig, ax = plt.subplots()
ax.set(ylim=(0.48,0.52))
sns.barplot(x='Role1',y='Totalwinrate',data=popchamp)

# #### From the above graph we can see that popular champions in jungle and mid roles made more impact on the game¶

fig, ax = plt.subplots()
ax.set(ylim=(0.48,0.52))
sns.barplot(x='Role1',y='Totalwinrate',data=df)

# #### On comparing with the previous graph we can see that, in general overall play though, support role played a more impactful game. This means that there is a lot more variance in support role winrates

optop = popchamp.copy()
optop = optop[popchamp['Role1']=='Top']

optop

fig, ax = plt.subplots()
ax.set(ylim=(0.48,0.52))
sns.barplot(x='Champions',y='Totalwinrate',data=optop)

sns.boxplot(x='Role1',y='Totalwinrate',data=popchamp,)

sns.boxplot(x='Role1',y='Totalwinrate',data=df,)


