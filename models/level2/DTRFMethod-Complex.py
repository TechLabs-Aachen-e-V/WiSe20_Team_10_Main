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

import numpy as npL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

df = pd.read_csv('../../data/processed/LOLOracleData_ChampStats.csv')

df.head()

tagcols = ['BToptags','BJngtags','BMidtags','BAdctags','BSuptags','RToptags','RJngtags','RMidtags','RAdctags','RSuptags']

tag_dummies = pd.get_dummies(df[tagcols])

tag_dummies.head(2)

df2 = pd.concat([df,tag_dummies],axis=1)

df2.head(2)

df2.drop(tagcols,axis=1,inplace=True)

df2.head(2)

# ### Lets perform Decision Trees and Random Forests

X = df2.drop('Winner',axis=1)
y = df2['Winner']

X.head(2)

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


