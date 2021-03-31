import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import re
from collections import Counter
from sklearn.ensemble import IsolationForest 
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import classification_report, accuracy_score

# f = open("ThunderbirdLog.txt", "r")
# contents = f.read()

# f.close()

# print(contents)

def isOutlier(string):
    if string[0] != '-':
        return 1
    return 0

limit = 0
extractedData = []

mylines = []                             # Declare an empty list named mylines.
with open ('Thunderbird.txt', 'rt') as myfile: # Open lorem.txt for reading text data
        for myline in myfile:                # For each line, stored as myline,
            mylines.append(myline)           # add its contents to mylines.
    
        
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

print(df)

# print(len(df['Time'].unique()))

# input = df['Time']
# c = Counter(input)

# print(c.items())

df['Message'] = df['Message'].astype('category').cat.codes
df['Time'] = df['Time'].astype('category').cat.codes
df['LogNum'] = df['LogNum'].astype('category').cat.codes
print(df)

# x = df.values #returns a numpy array
# min_max_scaler = preprocessing.MinMaxScaler()
# x_scaled = min_max_scaler.fit_transform(x)
# df = pd.DataFrame(x_scaled)
# df.columns = ['Time', 'Message', 'LogNum', 'isAnomaly']
# print(df)



# plt.scatter(df['isAnomaly'], df['Time'])
# plt.xlabel('isAnomaly')
# plt.ylabel('Time')
# print(plt.show())


X_train, X_test, y_train, y_test = train_test_split(df, df['isAnomaly'], test_size=0.3)
# Isolation Forest ----


X_outliers = df[df.isAnomaly == 1]

# training the model - ISOLATION FOREST
print('ISOLATION FOREST ------------------------------------------')

y = df['isAnomaly']

a = IsolationForest(contamination='auto', n_estimators=100) 
y_prediction1 = a.fit_predict(df.drop('isAnomaly',axis = 1)) # Fitting the model.
y_prediction1[y_prediction1 == 1] = 0 # Valid transactions are labelled as 0.
y_prediction1[y_prediction1 == -1] = 1 # Fraudulent transactions are labelled as 1.
errors1 = (y_prediction1 != y).sum() # Total number of errors is calculated.

print(errors1)
print(accuracy_score(y_prediction1,y))
print(classification_report(y_prediction1,y))

# clf = IsolationForest(contamination='auto', n_estimators=100)
# clf.fit(X_train)

# y_pred_train = clf.predict(X_train)
# y_pred_test = clf.predict(X_test)
# y_pred_outliers = clf.predict(X_outliers)


# # new, 'normal' observations ----
# print("Accuracy:", list(y_pred_test).count(1)/y_pred_test.shape[0])


# print("Accuracy:", list(y_pred_outliers).count(-1)/y_pred_outliers.shape[0])

# LOF
print('LOCAL OUTLIER FACTOR ------------------------------------------')
y = df['isAnomaly']

a = LocalOutlierFactor(contamination = 'auto')
y_prediction1 = a.fit_predict(df.drop('isAnomaly',axis = 1)) # Fitting the model.
y_prediction1[y_prediction1 == 1] = 0 # Valid transactions are labelled as 0.
y_prediction1[y_prediction1 == -1] = 1 # Fraudulent transactions are labelled as 1.
errors1 = (y_prediction1 != y).sum() # Total number of errors is calculated.

print(errors1)
print(accuracy_score(y_prediction1,y))
print(classification_report(y_prediction1,y))
