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
#st.slider(label, min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")  

  daygame = st.sidebar.toggle('Day Game')
  opponent = st.sidebar.selectbox('Opponent', all_teams, index=13) # default to LA Dodgers
  div_rank = st.sidebar.slider('Division Rank', min_value=1, max_value=5, value=1, step=1)
  gb = st.sidebar.slider('Games Behind', min_value=-5.0, max_value=5.0, value=0.0, step=0.50)
  st.sidebar.write('Note that negative games behind equals positive games ahead')

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
  
  data = {'daygame': daygame,
          'opponent': opponent,
          'div_rank': div_rank,
          'games_behind': gb,
          'al_east': al_east,
          'al_other': al_other,
          'nl': nl}

  features_df = pd.DataFrame(data, index=[0])
  return data, features_df

data, df = user_input_features()

st.subheader('User Input Parameters')
st.write(data)

st.write("""
# Predicted Attendance
""")

history = pd.read_csv('rays_attendance.csv')

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

scaler = StandardScaler()
scaler.fit_transform(hist)

regr = LinearRegression()
y = hist[['attendance']]
X = hist.drop(columns=['attendance'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

import numpy as np
regr.fit(X_train, y_train)

y_pred = regr.predict(X_test)

st.write(y_pred, " +/- ", int(np.round(np.sqrt(mean_absolute_error(y_test, y_pred)),-2))
