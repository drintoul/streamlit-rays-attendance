def get_games(**kwargs):
    """Get and format MLB games from baseball-reference.com
    """
    
    import pandas as pd
    from datetime import datetime
    import re
    
    names = {'HOU': 'Houston Astros', 'COL': 'Colorado Rockies', 'SFG': 'San Francisco Giants', 
         'CHW': 'Chicago White Sox', 'TOR': 'Toronto Blue Jays', 'BAL': 'Baltimore Orioles', 
         'BOS': 'Boston Red Sox', 'KCR': 'Kansas City Royals', 'ARI': 'Arizona Diamondbacks',
         'NYY': 'New York Yankees', 'MIA': 'Miami Marlins', 'LAD': 'Los Angeles Dodgers', 
         'CLE': 'Cleveland Guardians', 'MIN': 'Minnesota Twins', 'DET': 'Detroit Tigers', 
         'OAK': 'Oakland Athletics', 'LAA': 'Los Angeles Angels', 'TEX': 'Texas Rangers',
         'SEA': 'Seattle Mariners', 'SDP': 'San Diego Padres', 'WSN': 'Washington Nationals',
         'NYM': 'New York Mets', 'CHC': 'Chicago Cubs', 'ATL': 'Atlanta Braves',
         'PHI': 'Phildelphia Phillies', 'CIN': 'Cincinnati Reds', 'STL': 'St. Louis Cardinals',
         'MIL': 'Milwaukee Brewers', 'PIT': 'Pittsburg Pirates'}
    
    df = pd.DataFrame()
    year = kwargs.get('year')
    
    # retrieve table
    dfs = pd.read_html(f'https://www.baseball-reference.com/teams/TBR/{year}-schedule-scores.shtml')
    df = dfs[0]

    # format
    df.drop(columns=['Gm#', 'Unnamed: 2', 'Tm', 'W/L', 'R', 'RA', 'Inn', 'W-L', 'Win', 'Loss', 'Save', 
                 'Time', 'cLI', 'Streak', 'Orig. Scheduled'], inplace=True)
    df = df[df['Rank'] != 'Rank']
    df['GB'] = df['GB'].apply(lambda x: x.replace('Tied', '0.0').replace('up ', ''))
    df['Opp'] = df['Opp'].map(names)
    df['Year'] = year
    df = df.rename(columns={'Unnamed: 4': 'H/A', 'Opp': 'Opponent'})
    
    df = df[['Date', 'Year', 'Opponent', 'H/A', 'Rank', 'GB', 'D/N', 'Attendance']]
    
    return df


import pandas as pd
import time

df = pd.DataFrame()

for year in range(2013, 2024):
    
    if year == 2020:
        continue

    data = get_games(year=year)
    df = pd.concat([df, data], axis=0)
    
    time.sleep(10)
    
df.to_csv('rays_attendance.csv', index=False)
