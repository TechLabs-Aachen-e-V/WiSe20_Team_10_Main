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

# # To determine the classification of Game results using Decision trees & Random Forests

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

df = pd.read_csv('../../data/processed/LOLOracleData_ChampStats.csv')

df.head()

print(df.columns)

req_cols = ['BTop','BJng','BMid','BAdc','BSup','RTop','RJng','RMid','RAdc','RSup','BTopWr','BJngWr','BMidWr','BAdcWr','BSupWr','RTopWr','RJngWr','RMidWr','RAdcWr','RSupWr','BToptags','BJngtags','BMidtags','BAdctags','BSuptags','RToptags','RJngtags','RMidtags','RAdctags','RSuptags','Winner']

columns = list(df.columns)

for i in range(len(req_cols)):
    columns.remove(req_cols[i])

columns

df.drop(columns,axis=1,inplace=True)

df

df2 = pd.read_csv('../../data/processed/LOLOracleDatawithSynscores.csv')

df2.head()

df2.columns

df2.drop(['BTop', 'BJng', 'BMid', 'BAdc', 'BSup', 'RTop', 'RJng', 'RMid', 'RAdc',
       'RSup', 'Winner'],axis=1,inplace=True)

df = pd.concat([df,df2],axis=1)

df.head(50)

df.head()

df.drop(['BTop', 'BJng', 'BMid', 'BAdc', 'BSup', 'RTop', 'RJng', 'RMid', 'RAdc',
       'RSup'],axis=1,inplace=True)

df.head()

df.columns

taglist = list(df['BToptags'].unique())

taglist

len(taglist)

taglistencode = np.arange(0,13)

taglist2encode = zip(taglist,taglistencode)
taglist2encode = dict(taglist2encode)

taglist2encode

tagcols = ['BToptags','BJngtags','BMidtags','BAdctags','BSuptags','RToptags','RJngtags','RMidtags','RAdctags','RSuptags']            

for j in tagcols:
    df[j].replace(taglist2encode,inplace=True)

df

df.columns

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

from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier(n_estimators=200)


rfc.fit(X_train,y_train)

predict_rfc = rfc.predict(X_test)

print (confusion_matrix(y_test,predict_rfc))
print('\n')
print(classification_report(y_test,predict_rfc))


