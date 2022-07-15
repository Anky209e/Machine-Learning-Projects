import pandas as pd
import numpy as np
import os

data_frame_main = pd.read_csv("data.csv")
dataset=pd.read_csv('data.csv')

data_frame_main['timestamp'] = pd.to_datetime(data_frame_main['timestamp'], errors='coerce')

data_frame_main['timestamp'] = pd.to_datetime(data_frame_main['timestamp'], format = '%d/%m/%Y %H:%M:%S')

column_1 = data_frame_main.iloc[1:,0]

db=pd.DataFrame({"year": column_1.dt.year,
              "month": column_1.dt.month,
              "day": column_1.dt.day,
              "hour": column_1.dt.hour,
              "dayofyear": column_1.dt.dayofyear,
              "week": column_1.dt.week,
              "weekofyear": column_1.dt.weekofyear,
              "dayofweek": column_1.dt.dayofweek,
              "weekday": column_1.dt.weekday,
              "quarter": column_1.dt.quarter,
             })

dataset1=dataset.drop('timestamp',axis=1)
data1=pd.concat([db,dataset1],axis=1)
data1.dropna(inplace=True)
file = "main_data.csv"
if file in os.listdir(os.getcwd()):
    print("Already Present")
else:
    data1.to_csv(file,index=False)
    print("File saved")