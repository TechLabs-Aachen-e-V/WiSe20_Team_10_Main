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
import tqdm # <- tqdm is a handy small package to get a progress bar of for-loops :) Just do `pip install tqdm`
# %matplotlib inline


df = pd.read_csv('../data/processed/LOLOracleData.csv')

df.head()

rd = df.copy()        #to extract data we need to work on and to remove unwanted columns

rd.columns

rd.drop(['server', 'summoner_name','Time'],axis=1,inplace=True)

rd.head()

Blue = ['BTop', 'BJng', 'BMid', 'BAdc',
       'BSup']
Red = ['RTop', 'RJng', 'RMid', 'RAdc', 'RSup']

# +
#To determine Blue side and red side winrate

g = len(rd['winner'])   # Total number of games
b = len(rd[rd['winner']=='Blue'])     # No of games blue won
r = len(rd[rd['winner']=='Red'])      # No of games red won
bw = b/g
rw = r/g
# -

bw #Blue Winrate

rw #Red Winrate

# +
#Conclusion is that there is no discernable difference in the winrates of both sides

# +
#To determine now the winrate of each champion

# +
#To collect all the unique champion names

col = Blue + Red
champ= []
for i in col:
    tempchamp = rd[i].unique()
    champ = np.append(champ,tempchamp)
    
    
#Converting the data to a series to extract unique values and converting it back to a list    
temp = pd.Series(champ)
champions = temp.unique()
champions = list(champions)
# -

len(champions) #Total no of unique champions

# +
#Now we need to create a different dataset with all the champion winrates along with which side they were played
# -

cd = pd.DataFrame(champions,columns=['Champions'])   #cd - champion data




cd.head()

# +
# rd.head()

# +
#Example for one champion

countb=0
countbw=0
for j in Blue:
    for i in range(len(rd)):
        if(rd.loc[i,j]=='Camille'):
            if(rd.loc[i,'winner']=='Blue'):
                countbw = countbw+1
            countb = countb+1
cd.loc[cd['Champions']=='Camille','BlueWon'] =  countbw 
cd.loc[cd['Champions']=='Camille','BluePlayed'] = countb


countr=0
countrw=0
for j in Red:
    for i in range(len(rd)):
        if(rd.loc[i,j]=='Camille'):
            if(rd.loc[i,'winner']=='Red'):
                countrw = countrw+1
            countr = countr+1
cd.loc[cd['Champions']=='Camille','RedWon'] =  countrw 
cd.loc[cd['Champions']=='Camille','RedPlayed'] = countr
# -

cd.head()

# +
# An alternative way to do it saves many look-ups in the large dataframe (rd) and uses the ultra-fast
# native python datatype dictionary:

# 1. Set up the empty dictionaries with champion names as keys and one of the four counters as values.
#    We also now have the advantage that we know what we will do afterwards. We therefore record the roles as well.
blue_played = {champ: 0 for champ in champions}
blue_won = {champ: 0 for champ in champions}
red_played = {champ: 0 for champ in champions}
red_won = {champ: 0 for champ in champions}
roles = ['Top', 'Jng', 'Mid', 'Adc', 'Sup']
roles_played = {champ: {role: 0 for role in roles} for champ in champions}

# 2. Run through the rows of rd and then through all 10 roles (in two loops of 5 roles). Add to the counters of
#    the 10 champions that occur in the row with the correct logic for winning champs (boolean variables 
#    winner_is_blue and winner_is_red will be transformed to integers automatically):

for _row in tqdm.tqdm(rd.iterrows()): 
    row = _row[1]
    winner_is_blue = row.winner=='Blue'
    winner_is_red = not winner_is_blue
    for blue_role in Blue:
        champ = row[blue_role]
        blue_played[champ] += 1
        blue_won[champ] += winner_is_blue
        roles_played[champ][blue_role[1:]] += 1 # Strip the "B"/"R" from blue_role to get the role.
    for red_role in Red:
        champ = row[red_role]
        red_played[champ] += 1
        red_won[champ] += winner_is_red
        roles_played[champ][red_role[1:]] += 1 
        
# 3. Turn the dictionary into a dataframe: Make sure to refer to a *fixed-order* container with all champions.
#    If we don't, we will mess up the rows of the data frame because the four dictionaries are *not* ordered!
#    For the roles, we need some pre-processing to order how often which role was played

number_of_roles_to_record = 2 # We use 2 roles, could use up to all 5
ordered_roles_played = [[] for _ in range(number_of_roles_to_record)]
numbers_roles_played = [[] for _ in range(number_of_roles_to_record)]
for i, champ in enumerate(champions):
    # This is a list of tuples (role, #plays in the role):
    roles_for_this_champ = list(roles_played[champ].items()) 
    # sort by number of plays, in descending order (reverse=True)
    sorted_roles_for_this_champ = sorted(roles_for_this_champ, key=lambda x: x[1], reverse=True)
    
    # Now let's record the sorted tuples as order of most played roles (and their # of plays) 
    for j in range(number_of_roles_to_record):
        ordered_roles_played[j].append(sorted_roles_for_this_champ[j][0]) # Record the role
        numbers_roles_played[j].append(sorted_roles_for_this_champ[j][1]) # Record the # of plays
        
most_played_roles = {f"Role{j+1}": ordered_roles_played[j] for j in range(number_of_roles_to_record)}
most_played_numbers = {f"#Role{j+1}": numbers_roles_played[j] for j in range(number_of_roles_to_record)}

cd = pd.DataFrame({
    'Champion': champions,
    'BluePlayed': [blue_played[champ] for champ in champions],
    'BlueWon': [blue_won[champ] for champ in champions],
    'RedPlayed': [red_played[champ] for champ in champions],
    'RedWon': [red_won[champ] for champ in champions],
    **most_played_roles,
    **most_played_numbers,
})

# +
#For all champions (old version)

# for a in champions:
#     countb=0
#     countbw=0
#     for j in Blue:
#         for i in range(len(rd)):
#             if(rd.loc[i,j]==a):
#                 if(rd.loc[i,'winner']=='Blue'):
#                     countbw = countbw+1
#                 countb = countb+1
#     cd.loc[cd['Champions']==a,'BlueWon'] =  countbw 
#     cd.loc[cd['Champions']==a,'BluePlayed'] = countb


#     countr=0
#     countrw=0
#     for j in Red:
#         for i in range(len(rd)):
#             if(rd.loc[i,j]==a):
#                 if(rd.loc[i,'winner']=='Red'):
#                     countrw = countrw+1
#                 countr = countr+1
#     cd.loc[cd['Champions']==a,'RedWon'] =  countrw 
#     cd.loc[cd['Champions']==a,'RedPlayed'] = countr
    
# -

cd['TotalPlayed'] = cd['BluePlayed'] + cd['RedPlayed']

cd['Bluewinrate'] = cd['BlueWon'] / cd['BluePlayed']
cd['Redwinrate'] = cd['RedWon'] / cd['RedPlayed']
cd['Totalwinrate'] = (cd['BlueWon']+cd['RedWon'])/cd['TotalPlayed']



cd.head(3)

rd.head(3)

'BTop'.split('B')[1]

# +
Top = ['BTop','RTop']
Mid = ['BMid','RMid']
Jng = ['BJng','RJng']
Adc = ['BAdc','RAdc']
Sup = ['BSup','RSup']

Roles = [Top,Jng,Mid,Adc,Sup]

# +
#To find most commonly played roles for each champ
# +
#Example for one champion - old version, this is now done in the first loop already
# first=0
# second=0
# arole='None'
# brole='None'
# for j,k in Roles:
#     count=0
#     for i in range(len(rd)):
#         if(rd.loc[i,j]=='Vladimir'):
#             count=count+1
#         if(rd.loc[i,k]=='Vladimir'):
#             count=count+1
        
#     if count>first:
#         first = count
#         arole = j.split('B')[1]

# for j,k in Roles:
#     count=0
#     for i in range(len(rd)):
#         if(rd.loc[i,j]=='Vladimir'):
#             count=count+1
#         if(rd.loc[i,k]=='Vladimir'):
#             count=count+1
    
#     if count!=first:
#         if count>second:
#             second = count
#             brole = j.split('B')[1]
        
# cd.loc[cd['Champions']=='Vladimir','Role1'] = arole
# cd.loc[cd['Champions']=='Vladimir','Role2'] = brole
# cd.loc[cd['Champions']=='Vladimir','#Role1'] = first
# cd.loc[cd['Champions']=='Vladimir','#Role2'] = second

# -

first

second

arole

brole

cd.head()

# +
#For all champions - old version

# for a in champions:
#     first=0
#     second=0
#     arole='None'
#     brole='None'
#     for j,k in Roles:
#         count=0
#         for i in range(len(rd)):
#             if(rd.loc[i,j]==a):
#                 count=count+1
#             if(rd.loc[i,k]==a):
#                 count=count+1
        
#         if count>first:
#             first = count
#             arole = j.split('B')[1]

#     for j,k in Roles:
#         count=0
#         for i in range(len(rd)):
#             if(rd.loc[i,j]==a):
#                 count=count+1
#             if(rd.loc[i,k]==a):
#                 count=count+1
    
#         if count!=first:
#             if count>second:
#                 second = count
#                 brole = j.split('B')[1]
        
#     cd.loc[cd['Champion']==a,'Role1'] = arole
#     cd.loc[cd['Champion']==a,'Role2'] = brole
#     cd.loc[cd['Champion']==a,'#Role1'] = first
#     cd.loc[cd['Champion']==a,'#Role2'] = second
        


# -

cd.head()

cd.to_csv('ChampionStats.csv',index=False)

cd.head(3)

cd[['BlueWon','BluePlayed','RedWon','RedPlayed','TotalPlayed','#Role1','#Role2']] = cd[['BlueWon','BluePlayed','RedWon','RedPlayed','TotalPlayed','#Role1','#Role2']].astype(int)

cd.head(3)

cd = cd.round(6)

cd.to_csv('../data/processed/ChampionStats.csv',index=False)


