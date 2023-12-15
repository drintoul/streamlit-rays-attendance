import streamlit as st
import pandas as pd

st.write("""
# Rays Home Attendance Predictor
""")

capacity = 31042

al_east = ['Baltimore Orioles', 'Boston Red Sox', 'New York Yankees', 'Toronto Blue Jays', 'Tampa Bay Rays']
al_other = ['Chicago White Sox', 'Cleveland Guardians', 'Detroit Tigers', 'Kansas City Royals', 'Minnesota Twins',
            'Houston Astros', 'Los Angeles Angels', 'Oakland Athletics', 'Seattle Mariners', 'Texas Rangers']
nl = ['Atlanta Braves', 'Miami Marlins', 'New York Mets', 'Philadelphia Phillies', 'Washington Nationals',
      'Chicago Cubs', 'Cincinnati Reds', 'Milwaukee Brewers', 'Pittsburgh Pirates', 'St. Louis Cardinals',
      'Arizona Diamond Backs', 'Coloroado Rockies', 'Los Angeles Dodgers', 'San Diego Padres', 'San Francisco Giants']

all = al_east + al_other + nl

st.write(all)

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


  
