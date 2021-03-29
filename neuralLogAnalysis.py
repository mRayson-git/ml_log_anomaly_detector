
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import re
from collections import Counter
from sklearn import preprocessing
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import seaborn as sns


# Model imports
import keras
from keras.models import Sequential 
from keras.layers import Dense 
from keras.layers import LSTM
from keras.callbacks import Callback 
from keras import backend as K

import os
import tensorflow as tf


def isOutlier(string):
    if string[0] != '-':
        return 1
    return 0

limit = 0
extractedData = []

mylines = []                             # Declare an empty list named mylines.
with open ('Thunderbird.log', 'rt') as myfile: # Open lorem.txt for reading text data
    for myline in myfile:                # For each line, stored as myline,
        if(limit == 2000000):
            break
        mylines.append(myline)           # add its contents to mylines.
        limit += 1

    count = 0    
    temp = []
    for myline in mylines:                # For each line, stored as myline,
            if(myline[0] != '-'):
                count += 1
                temp.append(myline)
                if(count == 6000):
                    break
    normCount = 0
    for myline in mylines:
        if(myline[0] == '-'):
            normCount += 1
            temp.append(myline)
            if(normCount == 6000):
                break
    
    mylines = temp
    print(count)
    print(normCount)
    print(len(mylines))
    
    for element in mylines:
        isAnomaly = isOutlier(element)

        match = re.search(r'\d{2}:\d{2}:\d{2}',element)     # getting the time of log
        text = element.split(':')                           # splitting :
        
        code = element.split('2005')
       
        arr = []
        
        arr.append(match.group())
        if(text[-2].strip('') == ' Warning'):
            arr.append(text[-2] + ': ' + text[-1]) 
        else:
            arr.append(text[-1])                                # getting last element after : which is message

        arr.append(code[0])

        arr.append(isAnomaly)

        extractedData.append(arr)
        
        

df = pd.DataFrame(extractedData, columns = ['Time', 'Message', 'LogNum', 'isAnomaly'])

# - Evauluation functions ------------------------------
def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))
# ------------------------------------------------------

print(df)
df = df.sample(frac=1)
print(df)



# works - print(df)

df['Message'] = df['Message'].astype('category').cat.codes
df['Time'] = df['Time'].astype('category').cat.codes
df['LogNum'] = df['LogNum'].astype('category').cat.codes

# prints categorical representations - print(df)

# normalize the data between 0-1
x = df.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df = pd.DataFrame(x_scaled)
df.columns = ['Time', 'Message', 'LogNum', 'isAnomaly']

# shows time and anomaly correlation 
# plt.figure(figsize=(20,5))
# sns.scatterplot(df['Time'], df['isAnomaly'])


feature_cols = ['Time', 'Message']
X_train, X_test, y_train, y_test = train_test_split(df[feature_cols], df['isAnomaly'], test_size=0.3)


# model = keras.Sequential(
#  [
#  keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[-1],)),
#  keras.layers.Dense(128, activation='relu'),
#  keras.layers.Dropout(0.3),
#  keras.layers.Dense(256, activation='relu'),
#  keras.layers.Dropout(0.3),
#  keras.layers.Dense(1, activation='sigmoid'),
#  ]
# )

model = keras.Sequential(
 [
 keras.layers.Dense(2, activation='relu', input_shape=(X_train.shape[-1],)),
 keras.layers.Dense(8, activation='relu'),
 keras.layers.Dropout(0.3),
 keras.layers.Dense(16, activation='relu'),
 keras.layers.Dropout(0.3),
 keras.layers.Dense(1, activation='sigmoid'),
 ]
)
print(model.summary())

model.compile(
 optimizer='adam', 
 loss='mean_squared_error', 
 metrics=['accuracy', f1_m, precision_m, recall_m]
)

history = model.fit(
 X_train,
 y_train,
 batch_size=2048,
 epochs=15,
 verbose=2
)

y_pred = model.predict(X_test)
print()
print(confusion_matrix(y_test, y_pred.round()))
print()

# print('True:', y_test.values[0:25])
# print('False:', y_pred[0:25])
