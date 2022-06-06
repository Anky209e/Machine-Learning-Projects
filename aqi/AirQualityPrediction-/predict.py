import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
df = pd.read_csv("Data.csv")
df.fillna(method='ffill', inplace = True)
df = df[df.duplicated() == False]
X = df[['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM']]
y = df['PM 2.5']

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = 0.1, random_state = 35)
from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(X_train, y_train)

from sklearn import metrics


prediction = lr.predict(X_val)

print('MAE:', metrics.mean_absolute_error(y_val, prediction))
print('MSE:', metrics.mean_squared_error(y_val, prediction))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_val, prediction)))

def air_prediction(arr):
    lr.fit(X_train, y_train)
    prediction = lr.predict(X_val)
    print('MAE:', metrics.mean_absolute_error(y_val, prediction))
    print('MSE:', metrics.mean_squared_error(y_val, prediction))
    print('RMSE:', np.sqrt(metrics.mean_squared_error(y_val, prediction)))

    prediction = lr.predict(arr)
    
    return prediction
