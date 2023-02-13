import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from googleapiclient.discovery import build

# Use the YouTube Data API to get the channel statistics
def get_channel_statistics(channel_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.channels().list(part='statistics', id=channel_id)
    response = request.execute()
    return response['items'][0]['statistics']
     


#test code
channel_ids = ['UCvpfclapgcuJo0M_x65pfRw', #beebom
               'UCO2WJZKQoDW4Te6NHx4KfTg', #mrWTB
               'UCOhHO2ICt0ti9KAh-QHvttQ', #techguruji
               'UCsTcErHg8oDvUnTzoqsYeNw', #geekyranjit
               'UCMiJRAwDNSNzuYeN2uWa0pA'] #unboxtherapy
               
               
# Use the first channel ID as the default value
default_channel_id = channel_ids[0]


# Train a Random Forest regression model on the channel statistics
model = RandomForestRegressor(n_estimators=100)


st.title("YouTube Channel Publication Predictor")

# Get the API key from the user
api_key = st.text_input("Enter your YouTube Data API key:", "")


# Create a dropdown to select the channel ID
selected_channel_id = st.selectbox("Select a channel ID:", channel_ids, index=0)
     
     
if st.button("Get Channel Statistics"):
    statistics = get_channel_statistics(selected_channel_id, api_key)
    df = pd.DataFrame.from_dict(statistics, orient='index', columns=['Value'])
    df = df.reset_index().rename(columns={'index': 'Statistic'})
    df['Value'] = df['Value'].astype(int)
    prediction = model.predict(df)
    st.write("The model predicts the next publication will be in", int(prediction), "days")
    
    
st.write("Note: This prediction is based on the current channel statistics and may not reflect the actual publication date.")