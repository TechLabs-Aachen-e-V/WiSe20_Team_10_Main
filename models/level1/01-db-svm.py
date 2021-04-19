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

df = pd.read_csv('../../data/interim/EncodedLOLData.csv')

df.head(5)

# #### Lets try training the data without encoding every single champion using one hot enocder / dummies

from sklearn.model_selection import train_test_split

X = df.drop('Winner',axis=1)
y = df['Winner']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=101)

from sklearn.svm import SVC

svm = SVC()

svm.fit(X_train,y_train)

predictions = svm.predict(X_test)

from sklearn.metrics import classification_report,confusion_matrix

print(confusion_matrix(y_test,predictions))
print('\n')
print(classification_report(y_test,predictions))

# ### Lets try using Gridsearch to get the optimum values for hyperparameters C and Gamma

from sklearn.model_selection import GridSearchCV

params = {'C':[0.1,1,10,100,1000],'gamma':[1,0.1,0.01,0.001,0.0001]}

grid = GridSearchCV(SVC(),params,verbose=3)

grid.fit(X_train,y_train)

grid_predictions = grid.predict(X_test)

print(confusion_matrix(y_test,grid_predictions))
print('\n')
print(classification_report(y_test,grid_predictions))

# ### So we still end up getting a prediction score of 0.5
#
# ### Lets try again but now lets encode every single champion data

X = pd.get_dummies(data=df,columns=['BTop', 'BJng', 'BMid', 'BAdc', 'BSup', 'RTop', 'RJng', 'RMid', 'RAdc','RSup'])
y = df['Winner']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=101)

from sklearn.svm import SVC

svm = SVC()

svm.fit(X_train,y_train)

predictions = svm.predict(X_test)

from sklearn.metrics import classification_report,confusion_matrix

print(confusion_matrix(y_test,predictions))
print('\n')
print(classification_report(y_test,predictions))

# ### Lets try using Gridsearch to get the optimum values for hyperparameters C and Gamma

from sklearn.model_selection import GridSearchCV

params = {'C':[0.1,1,10,100,1000],'gamma':[1,0.1,0.01,0.001,0.0001]}

grid = GridSearchCV(SVC(),params,verbose=3)

grid.fit(X_train,y_train)

grid_predictions = grid.predict(X_test)

print(confusion_matrix(y_test,grid_predictions))
print('\n')
print(classification_report(y_test,grid_predictions))


