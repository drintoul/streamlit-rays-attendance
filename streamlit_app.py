import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
#from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

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

wschampions = ['Texas Rangers', 'Houston Astros', 'Atlanta Braves', 'Los Angeles Dodgers', 'Washington Nationals',
               'Chicago Cubs', 'Kansas City Royals', 'Boston Red Sox', 'Philadelphia Phillies', 'San Francisco Giants',
               'St. Louis Cardinals', 'New York Yankees']

# remember to take Tampa Bay Rays out of list of opponents
all_teams = sorted(al_east_teams[:-1] + al_other_teams + nl_teams)

st.sidebar.header('User Input Parameters')

def user_input_features():
#st.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")  

  daygame = st.sidebar.toggle('Day Game')
  div_rank = st.sidebar.slider('Division Rank', min_value=1, max_value=5, value=1, step=1)
  gb = st.sidebar.slider('Games Behind', min_value=-5.0, max_value=5.0, value=0.0, step=0.50)
  st.sidebar.write('Note that negative games behind equals positive games ahead')
  opponent = st.sidebar.selectbox('Opponent', all_teams, index=13) # default to LA Dodgers

  if opponent in al_east_teams:
    al_east = True
  else:
    al_east = False

  if opponent in al_other_teams:
    al_other = True
  else:
    al_other = False

  if opponent in nl_teams:
    nl = True
  else:
    nl = False

  if opponent in wschampions:
    wschamps = True
  else:
    wschamps = False

  if opponent == 'New York Yankees':
    yankees = True
  else:
    yankees = False

  if opponent == 'Boston Red Sox':
    redsox = True
  else:
    redsox = False

  data = {'daygame': daygame,
          'div_rank': div_rank,
          'games_behind': gb,
          'opponent': opponent,
          'al_east': al_east,
          'al_other': al_other,
          'nl': nl,
          'wschamps': wschamps,
          'yankees': yankees,
          'redsox': redsox}

  features_df = pd.DataFrame(data, index=[0])
  return data, features_df

data, df = user_input_features()

st.subheader('Machine Learning model based on 2008-2023 inclusive home games (not including 2020)')

st.subheader('User Input Parameters')
st.write(data)

df = pd.read_csv('rays_attendance.csv')

df['al_east'] = df['Opponent'].apply(lambda x: True if x in al_east_teams else False)
df['al_other'] = df['Opponent'].apply(lambda x: True if x in al_other_teams else False)
df['nl'] = df['Opponent'].apply(lambda x: True if x in nl_teams else False)
df['wschamps'] = df['Opponent'].apply(lambda x: True if x in wschampions else False)
df['yankees'] = df['Opponent'].apply(lambda x: True if x == 'New York Yankees' else False)
df['redsox'] = df['Opponent'].apply(lambda x: True if x == 'Boston Red Sox' else False)

df = df[df['H/A'].isnull()]
df = df.reindex()
df = df[['Rank', 'GB', 'D/N', 'al_east', 'al_other', 'nl', 'wschamps', 'yankees', 'redsox', 'Attendance']]
df.columns = ['div_rank', 'games_behind', 'daygame', 'al_east', 'al_other', 'nl', 'wschamps', 'yankees', 'redsox', 'attendance']
df['daygame'] = df['daygame'] == 'D'

df = df.sample(frac=1)
df = df.reset_index(drop=True)

#st.write("""
# Data for ML Model Development
#""")

#st.dataframe(df.head(), hide_index=True, use_container_width=True)
#st.write(df.describe())

st.write("""
# Predicted Attendance
""")

st.markdown('<p class="big-font">Hello World !!</p>', unsafe_allow_html=True)
