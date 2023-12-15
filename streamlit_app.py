import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
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
  div_rank = st.sidebar.slider('Ray\'s AL East Division Rank before game', min_value=1, max_value=5, value=1, step=1)
  gb = st.sidebar.slider('Games Behind Division Leader before game', min_value=-5.0, max_value=10.0, value=0.0, step=0.50)
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

  features = pd.DataFrame(data, index=[0])
  return data, features

data, features = user_input_features()

# Train Model

df = pd.read_csv('rays_attendance.csv')

min = df[df['H/A'].isnull()]'Attendance'].min()
max = df[df['H/A'].isnull()]'Attendance'].max()

mm_df = df[df['H/A'].isnull()].loc[df['Attendance'].agg(['idxmin','idxmax']) ]
mm_df = mm_df.drop(columns=['H/A']

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

X = df.iloc[:,:-1]
y = df.iloc[:,-1]
scaler = StandardScaler().fit(X)
X = scaler.transform(X)

model = LinearRegression().fit(X, y)
y_pred = model.predict(X)
error = mean_absolute_error(y_pred, y)

# Apply Model to User Input

features = pd.DataFrame(data, index=[0])
features.drop(columns=['opponent'], inplace=True)
X1 = np.array(features)
scaler.transform(X1)

prediction = model.predict(X1)[0]

st.write('Machine Learning model based on 2008-2023 inclusive regular season home games (not including 2020)')

st.dataframe(mm_df, hide_index=True)

st.write(f'With crowds as small as {min:,} and as large as {max:,}, it\'s important to be able to predict attendance to plan promotions and giveaways', unsafe_allow_html=True)
st.write('Select input parameters using sidebar on the left')

st.subheader('User Input Parameters')
st.write(data)

st.write("""
# Predicted Attendance
""")

st.markdown(f'<h3 class="big-font" color="green" font-weight="bold">{round(prediction,-2):,.0f} +/- {round(error,-3):,.0f}</h3>', unsafe_allow_html=True)
