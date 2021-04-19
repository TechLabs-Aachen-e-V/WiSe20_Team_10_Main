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

df = pd.read_csv('../../data/processed/LOLOracleDataWr.csv')

df.head()

df.columns

Red = ['RTop', 'RJng', 'RMid', 'RAdc','RSup']
Blue = ['BTop', 'BJng', 'BMid', 'BAdc', 'BSup']

for i in Red:
    df[i]=-df[i]

df.head()

# +
#For all entries with Blue = 1 and Red = -1

for i in range(len(df)):
    if df.loc[i,'Winner']==0:
        df.loc[i,'Winner']=1
    else:
        df.loc[i,'Winner']=-1
        
df['Winner'] = df['Winner'].astype(int)
# -

df.head()

# ### Lets implement KNN model now

from sklearn.model_selection import train_test_split

X = df.drop('Winner',axis=1)
y = df['Winner']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=101)

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=1)

knn.fit(X_train,y_train)

predictions = knn.predict(X_test)

from sklearn.metrics import confusion_matrix,classification_report

print(confusion_matrix(y_test,predictions))
print('\n')
print(classification_report(y_test,predictions))

# +
#Lets choose a K value now

# +
error_rate = []

for i in range(1,100):
    
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train,y_train)
    pred_i = knn.predict(X_test)
    error_rate.append(np.mean(pred_i != y_test))
# -

plt.figure(figsize=(10,6))
plt.plot(range(1,100),error_rate,color='blue', linestyle='dashed', marker='o',
         markerfacecolor='red', markersize=10)
plt.title('Error Rate vs. K Value')
plt.xlabel('K')
plt.ylabel('Error Rate')

knn = KNeighborsClassifier(n_neighbors=64)

knn.fit(X_train,y_train)

predictions = knn.predict(X_test)

from sklearn.metrics import confusion_matrix,classification_report

print(confusion_matrix(y_test,predictions))
print('\n')
print(classification_report(y_test,predictions))


