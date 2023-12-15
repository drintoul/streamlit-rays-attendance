import streamlit as st
import pandas as pd

st.write("""
# Rays Home Attendance Predictor
""")

capacity = 31042

al_east_teams = ['Baltimore Orioles', 'Boston Red Sox', 'New York Yankees', 'Toronto Blue Jays', 'Tampa Bay Rays']
al_other_teams = ['Chicago White Sox', 'Cleveland Guardians', 'Detroit Tigers', 'Kansas City Royals', 'Minnesota Twins',
                  'Houston Astros', 'Los Angeles Angels', 'Oakland Athletics', 'Seattle Mariners', 'Texas Rangers']
nl_teams = ['Atlanta Braves', 'Miami Marlins', 'New York Mets', 'Philadelphia Phillies', 'Washington Nationals',
            'Chicago Cubs', 'Cincinnati Reds', 'Milwaukee Brewers', 'Pittsburgh Pirates', 'St. Louis Cardinals',
            'Arizona Diamond Backs', 'Coloroado Rockies', 'Los Angeles Dodgers', 'San Diego Padres', 'San Francisco Giants']

all_teams = sorted(al_east_teams[:-1] + al_other_teams + nl_teams)

st.sidebar.header('User Input Parameters')

def user_input_features():

  day = st.sidebar.toggle('Day Game')
  opponent = st.sidebar.selectbox('Opponent', all)

  if 
  data = {'day': day,
          'opponent': opponent}

  features = pd.DataFrame(data, index=[0])
  return features

df = user_input_features()

st.subheader('User Input Parameters')
st.write(df)

if df['opponent'] in al_east_teams:
  al_east = True
else:
  al_east = False

if df['opponent'] in al_other_teams:
  al_other = True
else:
  al_other = False

if df['opponent'] in nl_teams:
  nl = True
else:
  nl = False

st.write(al_east)
st.write(al_other)
st.write(nl)
