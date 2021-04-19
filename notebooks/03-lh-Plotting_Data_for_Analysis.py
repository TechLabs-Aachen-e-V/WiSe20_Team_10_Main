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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

# Read the ChampionsStats CSV and sort Index by their main roles, in champStats_Role1
champStats = pd.read_csv("../data/processed/DataChampTemp.csv")
champStats_Role1 = champStats.set_index('Role1')
champStats_Champions = champStats.set_index('Champions')

champStats_Role1.head()



# Melt BlueWon and RedWon together for easier processing, get rid of other columns
champStats_melt = pd.melt(champStats_Role1,ignore_index=False, id_vars =['Champions','#Role1','TotalPlayed'], value_vars =['BlueWon','RedWon'],
              var_name ='WinningSide', value_name ='AmountWon')

# Create Data Frames for all Champions in their primary played Roles
topChamps = champStats_melt.loc['Top']
midChamps = champStats_melt.loc['Mid']
jngChamps = champStats_melt.loc['Jng']
adcChamps = champStats_melt.loc['Adc']
supChamps = champStats_melt.loc['Sup']

# Select the Top 20 played champions for each of these roles (largest 40 due to double entry caused by melting)
topChampsMVP = topChamps.nlargest(39, columns=['#Role1'])
midChampsMVP = midChamps.nlargest(40, columns=['#Role1'])
jngChampsMVP = jngChamps.nlargest(40, columns=['#Role1'])
adcChampsMVP = adcChamps.nlargest(40, columns=['#Role1'])
supChampsMVP = supChamps.nlargest(40, columns=['#Role1'])

# + language="html"
# <h2>Plotting Blue vs. Red Side Wins</h2>
#
# <p>
# The following plots display whether the top 20 Champions of each role (Top, Mid, Jng, Adc, Sup) achieved more wins
# on the red or blue side
# <br><br>
# Due to the fact that the Blue Side receives the first pick, the most popular/strongest
# Champions should by default have a higher winrate on the Blue Side.
# <br>
# Other than that, the Red Side should be more favorable
# for the Bot lane (ADC) and the Blue Side for Top lane (Top).
# <br><br>
# Therefore:<br>
#     <ul>
#     <li>The most popular Champion of each role will always have more wins on the Blue Side. This is due to the fact that the Blue Side picks first and the Red Side will more likely counterpick.</li>
#     <li>ADCs should have a higher win rate when they where played on the Red Side</li>
#     <li>Top Champions should have a higher winrate on the Blue Side - Except when the player on the Red Side selected a Counterpick that outmatches them</li>
#     </ul>
# </p>
# -

# Display whether Top Champions won more often on the blue or red side
g = sns.catplot(
    data=topChampsMVP, kind="bar",
    x="AmountWon", y="Champions", hue="WinningSide",
    ci="sd", palette=sns.color_palette(['#000080', '#FF6347']), alpha=.9, height=6,
)
g.despine(left=True)
g.set_axis_labels("Amount of Games won","Top Champions")
g.fig.suptitle('Blue vs Red Wins for Top 20 Top Champs', y=1)

# Display whether Mid Champions won more often on the blue or red side
g = sns.catplot(
    data=midChampsMVP, kind="bar",
    x="AmountWon", y="Champions", hue="WinningSide",
    ci="sd", palette=sns.color_palette(['#000080', '#FF6347']), alpha=.9, height=6,
)
g.despine(left=True)
g.set_axis_labels("Amount of Games won","Mid Champions")
g.fig.suptitle('Blue vs Red Wins for Top 20 Mid Champs', y=1)

# Display whether Jungler Champions won more often on the blue or red side
g = sns.catplot(
    data=jngChampsMVP, kind="bar",
    x="AmountWon", y="Champions", hue="WinningSide",
    ci="sd", palette=sns.color_palette(['#000080', '#FF6347']), alpha=.9, height=6,
)
g.despine(left=True)
g.set_axis_labels("Amount of Games won","Jng Champions")
g.fig.suptitle('Blue vs Red Wins for Top 20 Jng Champs', y=1)

# Display whether Adc Champions won more often on the blue or red side
g = sns.catplot(
    data=adcChampsMVP, kind="bar",
    x="AmountWon", y="Champions", hue="WinningSide",
    ci="sd", palette=sns.color_palette(['#000080', '#FF6347']), alpha=.9, height=6,
)
g.despine(left=True)
g.set_axis_labels("Amount of Games won","ADC Champions")
g.fig.suptitle('Blue vs Red Wins for Top 20 ADC Champs', y=1)

# Display whether Support Champions won more often on the blue or red side
g = sns.catplot(
    data=supChampsMVP, kind="bar",
    x="AmountWon", y="Champions", hue="WinningSide",
    ci="sd", palette=sns.color_palette(['#000080', '#FF6347']), alpha=.9, height=6,
)
g.despine(left=True)
g.set_axis_labels("Amount of Games won","Sup Champions")
g.fig.suptitle('Blue vs Red Wins for Top 20 Sup Champs', y=1)

# + language="html"
# <h2>Plotting Blue vs. Red Side Plays without Roles</h2>
#
# <p>
# Hypothesis: The Blue Side picks first and will therefore more likely take the strongest Champs, while Red will focus on doing Counterpicks
# <br><br>
# Deepak: So for example, if Renekton was played 2000 games and if we see that it has been played atleast 100 games more on Blue side compared to Red side, then we can say that it has been picked more on the Blue side because Renekton was a strong champ in this meta and because Blue side gets to pick first, they took away the champion from Red side
# <br>
# Result: From Plays alone doesnt seem that way with this data set
# </p>
# -

champStats_topChoices = champStats.set_index('TotalPlayed')

champStats_topChoicesBlue = champStats_topChoices.loc[(champStats_topChoices['BluePlayed']-champStats_topChoices['RedPlayed'] >= 100)]

champStats_topChoicesRed = champStats_topChoices.loc[(champStats_topChoices['RedPlayed']-champStats_topChoices['BluePlayed'] >= 100)]

champStats_topChoicesBlue

champStats_topChoicesRed

# + language="html"
# <h2>Champion Synergies</h2>
# <p>
# Checking which Champions played in a Team with other Champions
#
# </p>
# -

championSynergiesRaw = pd.read_csv('../Data/LOLOracleData.csv')
championSynergiesRaw = championSynergiesRaw.drop(columns=['server', 'summoner_name','Time'])
championSynergiesRaw = championSynergiesRaw.set_index('winner')

# I am separating red and blue team here to be able to deal better with the data
championsRedSide = championSynergiesRaw[['RTop','RJng','RMid','RAdc','RSup']].copy()  # just as thought for a later point

championsBlueSide = championSynergiesRaw[['BTop','BJng','BMid','BAdc','BSup']].copy() # just as thought for a later point

championsBlueSide.head()

# +
# Stole from Analysis.py to have all unique Champion names again

col = ['BTop', 'BJng', 'BMid', 'BAdc', 'BSup', 'RTop', 'RJng',
       'RMid', 'RAdc', 'RSup']
champ= []
for i in col:
    tempchamp = championSynergiesRaw[i].unique()
    champ = np.append(champ,tempchamp)


#Converting the data to a series to extract unique values and converting it back to a list
temp = pd.Series(champ)
champions = temp.unique()
champions = list(champions)
# -



numbersForChamps = [*range(0, 153, 1)] # create list of numbers to create a dictionnaire together with champ names

zip_iterator = zip(champions, numbersForChamps) # and now made a user-friendly dict by zipping both together
championToNumberDict = dict(zip_iterator) # and voila, done
numberToChampionDict = {v: k for k, v in championToNumberDict.items()} # and ro reverse it again in the final list

#arrayForSynergyLoop = np.array(shape=(153,153)) # declare array to save matches
arrayForSynergyLoop = np.zeros((153,153), int)

# Rename columns to create up one big dataframe (if not changed blue won't append right)
redColumnsRename = championsRedSide.rename(columns={'RTop':'Top','RJng':'Jng','RMid':'Mid','RAdc':'Adc','RSup':'Sup'})
blueColumnsRename = championsBlueSide.rename(columns={'BTop':'Top','BJng':'Jng','BMid':'Mid','BAdc':'Adc','BSup':'Sup'})

allChampionTeams = redColumnsRename.append(blueColumnsRename) # create one big dataframe of blue and red to count all synergies

allChampionTeams.head()

allChampionTeams.replace(championToNumberDict, inplace=True) # replace Champion names with numbers so that it runs faster

allChampionTeams.head()

allChampionTeamsDict=allChampionTeams.to_dict('records')

allChampionTeamsDict

for row in allChampionTeamsDict:
    for key, value in row.items():
        print(key,value)

# +
# Turn this into function

for row in allChampionTeams.itertuples(index=False):
    print(row)
    break
    i = 0

    while i < 5: # While i is smaller than 5 (since we only need to go through rows 0 to 4) check matches between i and y
        y = 0 # y is the potential 5 other match partners and increases by 1 each loop

        while y < 5: # i only increases after the last row of y in current loop went through
            I = [row[i]]
            J = [row[y]]
            if I == J:
                arrayForSynergyLoop[I,J] = arrayForSynergyLoop[I,J]-1
            else:
                arrayForSynergyLoop[I,J] = arrayForSynergyLoop[I,J]+1 # count up at correct coordinates when Synergy was found
            y = y + 1

        i = i + 1
# -

# Put the Array back into a DataFrame and rename index and columns back to the champion names
arrayForSynergyLoop_df = pd.DataFrame(arrayForSynergyLoop)
synergies = arrayForSynergyLoop_df.rename(index=numberToChampionDict,columns=numberToChampionDict)

synergies.head()

# +
# synergies.to_csv('../Data/ChampionSynergies.csv',index=True) # save file
# -
synergies[synergies < 0]=np.nan

synergies.head()

synergies.iloc[0].nlargest(4)

synergies.iloc[50].nlargest(4)

synergies.iloc[85].nlargest(4)

# +
sns.set_theme(style="white")

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(synergies, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(50, 50))

# Generate a custom diverging colormap
cmap = sns.color_palette("magma", as_cmap=True)

synergies.sort_values(axis='columns')
# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(synergies, cmap=cmap,
            square=True, linewidths=.5)
# -





