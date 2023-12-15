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

  daygame = st.sidebar.toggle('Day Game')
  opponent = st.sidebar.selectbox('Opponent', all_teams)

  data = {'daygame': daygame,
          'opponent': opponent}

  features = pd.DataFrame(data, index=[0])
  return features

df = user_input_features()

if df['opponent'][0] in al_east_teams:
  df['AL East'] = True
else:
  df['AL East'] = False

if df['opponent'][0] in al_other_teams:
  df['AL Other'] = True
else:
  df['AL Other'] = False

if df['opponent'][0] in nl_teams:
  df['NL'] = True
else:
  df['NL'] = False

st.subheader('User Input Parameters')
st.write(df)
