# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.8.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # To determine the classification of Game results using Decision trees & Random Forests

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

df = pd.read_csv('../../data/processedLOLOracleData.csv')

df.head()

df.drop(['server','summoner_name','Time'],axis=1,inplace=True)

df.head()

# ### To collect all the unique champion names

# +


col = ['BTop', 'BJng', 'BMid', 'BAdc', 'BSup', 'RTop', 'RJng',
       'RMid', 'RAdc', 'RSup']
champ= []
for i in col:
    tempchamp = df[i].unique()
    champ = np.append(champ,tempchamp)
    
    
#Converting the data to a series to extract unique values and converting it back to a list    
temp = pd.Series(champ)
champions = temp.unique()
champions = list(champions)
# -

# ### Encoding champion name into numbers in order to make it easier for processing

# +


#For one champion

for i in range(len(df)):
    for j in col:
        if(df.loc[i,j]=='Camille'):
            df.loc[i,j]=1
            
# -

df.head()

# +
#For all champions

for k in range(len(champions)):
    for i in range(len(df)):
        for j in col:
            if(df.loc[i,j]==champions[k]):
                df.loc[i,j]=k
            
# -

df.head()

# +
#For all entries with Blue = 0 and Red = 1

for i in range(len(df)):
    if df.loc[i,'winner']=='Blue':
        df.loc[i,'Winner']=0
    else:
        df.loc[i,'Winner']=1
        
df['Winner'] = df['Winner'].astype(int)
# -

df.head()

df.drop('winner',axis=1,inplace=True)

df.head()

# ### Note that the above process of encoding champion names takes close to 7 mins. To prevent doing that action every single time, the converted data is exported

df.to_csv('../../data/interim/EncodedLOLData.csv',index=False) #Exporting the encoded data for further processing

# ### Lets perform Decision Trees and Random Forests

X = df.drop('Winner',axis=1)
y = df['Winner']

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=101)

from sklearn.tree import DecisionTreeClassifier

dtc = DecisionTreeClassifier()


dtc.fit(X_train,y_train)

predict_dtc = dtc.predict(X_test)

from sklearn.metrics import classification_report,confusion_matrix

print (confusion_matrix(y_test,predict_dtc))
print('\n')
print(classification_report(y_test,predict_dtc))

# ### The results above show that for Decision Trees the precision isnt better than random chance. :(

from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier(n_estimators=300)


rfc.fit(X_train,y_train)

predict_rfc = rfc.predict(X_test)

print (confusion_matrix(y_test,predict_rfc))
print('\n')
print(classification_report(y_test,predict_rfc))

# ### Unfortunately even Random Forests dont seem promising

# ### Possibly the next step we can do is encode every single champion name into a dummy variable and try it







X = pd.get_dummies(df[['BTop', 'BJng', 'BMid', 'BAdc', 'BSup', 'RTop', 'RJng', 'RMid', 'RAdc','RSup']])
y = df['Winner']

X.head()

X.shape

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=101)

from sklearn.tree import DecisionTreeClassifier

dtc = DecisionTreeClassifier()


dtc.fit(X_train,y_train)

predict_dtc = dtc.predict(X_test)

from sklearn.metrics import classification_report,confusion_matrix

print (confusion_matrix(y_test,predict_dtc))
print('\n')
print(classification_report(y_test,predict_dtc))

from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier(n_estimators=300)


rfc.fit(X_train,y_train)

predict_rfc = rfc.predict(X_test)

print (confusion_matrix(y_test,predict_rfc))
print('\n')
print(classification_report(y_test,predict_rfc))
