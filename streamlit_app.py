import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error

st.set_page_config(page_title="Rays Home Attendance Predictor")
st.title("""Rays Home Attendance Predictor""")

# League Info
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

# Sort teams for drop down & Remember to take Tampa Bay Rays out of list of opponents
all_teams = sorted(al_east_teams[:-1] + al_other_teams + nl_teams)

st.sidebar.header('User Input Parameters')

# Function to collect input from sidebar
def user_input_features():

  daygame = st.sidebar.toggle('Day Game')
  div_rank = st.sidebar.slider('Ray\'s AL East Division Rank before game', min_value=1, max_value=5, value=2, step=1)
  gb = st.sidebar.slider('Games Behind Division Leader before game', min_value=-5.0, max_value=10.0, value=1.5, step=0.50)
  st.sidebar.info('negative games behind = games ahead', icon='ℹ️')
  opponent = st.sidebar.selectbox('Opponent', all_teams, index=13) # default to LA Dodgers

  # Build features
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

def main():

  data, features = user_input_features()

  # Train Model
  df = pd.read_csv('rays_attendance.csv', dtype={'Year': str})

  minimum = df[df['H/A'].isnull()][['Attendance']].min().values[0]
  maximum = df[df['H/A'].isnull()][['Attendance']].max().values[0]

  mm_df = df[df['H/A'].isnull()]
  mm_df = mm_df[(mm_df['Attendance'] == minimum) | (mm_df['Attendance'] == maximum)]
  mm_df = mm_df.drop(columns=['H/A'])

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

  # Scale input
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

  st.dataframe(mm_df, hide_index=True)

  st.write(f"""
  With crowds as small as {minimum:,} and as large as {maximum:,}, it\'s important to be able to predict attendance to plan promotions and giveaways. 
  Machine Learning model based on 2008-2023 inclusive regular season home games (not including Pandemic year of 2020 when games were played without fans in attendance).
  """, unsafe_allow_html=True)

  st.info('Select input parameters using sidebar to activate prediction', icon='ℹ️')

  st.subheader('User Input Parameters')
  st.write(data)

  st.write("""
  # Predicted Attendance
  """)

  st.markdown(f"hosting {data['opponent']} while ranked #{data['div_rank']} in AL East & being {data['games_behind']} games behind division lead.", unsafe_allow_html=True)

  st.markdown(f"<h3 class='big-font' color='green' font-weight='bold'>{round(prediction,-2):,.0f} +/- {round(error,-3):,.0f}</h3>", unsafe_allow_html=True)

  st.warning('Some combinations don\'t make \'sense\' - the Rays can\'t be in first place but 10 games behind. This happens when the model is used outside of its regular context.', icon='⚠️')

if __name__ == '__main__':
    main()
