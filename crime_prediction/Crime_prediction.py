import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
from predict_crime import predict


st.title("Location Based Crime Prediction")
st.image("https://hhsadvocate.com/wp-content/uploads/2021/12/TrueCrime-2.jpeg")
st.markdown("***")


a,b,c = st.columns(3)
year = c.number_input(label="Enter Year",value=2022,min_value=1900,max_value=3000)

date_in = a.number_input("Enter Date",value=29,max_value=31,min_value=1)

month_in = b.number_input("Enter Month",value=7,max_value=12,min_value=1)

min_in = b.number_input(label="Minutes",value=15,max_value=59,min_value=0)

hour_in = a.number_input(label="Hour",value=23,max_value=23,min_value=0)

sec_in = c.number_input(label="Seconds",value=0,max_value=59,min_value=0)

c,d = st.columns(2)
latitude = c.number_input(label="Latitude",value=22.720992,format="%f")
longitude = d.number_input(label="Longitude",value=75.876083,format="%f")

enter = st.button(label="Predict Crime")

st.markdown("***")
if enter:
    if len(str(month_in)) == 1:
        month_in = "0"+str(month_in)
    if len(str(hour_in)) == 1:
        hour_in = "0"+str(hour_in)
    if len(str(sec_in)) == 1:
        sec_in = "0"+str(sec_in)

    main_date = '-'.join([str(year),str(month_in),str(date_in)])
    main_time = ':'.join([str(hour_in),str(min_in),str(sec_in)])

    date_time = " ".join([main_date,main_time])
    
    sr = pd.Series([date_time])
    sr = pd.to_datetime(sr)
    print(sr)
    print(type(sr.dt.month))

    main_ins = {
              "month": sr.dt.month.tolist()[0],
              "day": sr.dt.day.tolist()[0],
              "hour": sr.dt.hour.tolist()[0],
              "dayofyear": sr.dt.dayofyear.tolist()[0],
              "week": sr.dt.week.tolist()[0],
              "weekofyear": sr.dt.weekofyear.tolist()[0],
              "dayofweek": sr.dt.dayofweek.tolist()[0],
              "weekday": sr.dt.weekday.tolist()[0],
              "quarter": sr.dt.quarter.tolist()[0],
             }
    inputs = list(main_ins.values())
    inputs.append(latitude)
    inputs.append(longitude)

    inputs_arr = np.array(inputs)

    labels = ['Robbery','Gambling','Accident','Violence','Murder','Kidnapping']
    vals,dicts = predict(inputs_arr)
    # print(list(vals.values()))
    explode = (0.2, 0.2, 0.2, 0.2,0.2,0.2)
    plt.pie(vals,labels=labels,explode=explode,shadow=True,autopct='%1.2f%%')
    plt.savefig('images/predict_graph.png')

    st.markdown("> Probablity of types of crimes happening on {} at {}".format(main_date,main_time))
    st.image('images/predict_graph.png')
    st.markdown("> Acts of Crime")
    st.write(dicts)
    