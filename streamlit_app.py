import streamlit as st
import pandas as pd

st.write("""
# Rays Home Attendance Predictor
""")

st.sidebar.header('User Input Parameters')

def user_input_features():

  day = st.sidebar.toggle('Day Game')
  opponent = st.sidebar.selectbox('Opponent', ('BOS', 'NYY', 'TOR'))

  data = {'day': day,
          'opponent': opponent}

  features = pd.DataFrame(data, index=[0])
  return features

df = user_input_features()

st.subheader('User Input Parameters')
st.write(df)


  
