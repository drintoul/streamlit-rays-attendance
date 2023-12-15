def get_games(**kwargs):
    """Get and format MLB games from baseball-reference.com
    """
    
    import pandas as pd
    
    df = pd.DataFrame()
    year = kwargs.get('year')
    
    dfs = pd.read_html(f'https://www.baseball-reference.com/teams/TBR/{year}-schedule-scores.shtml')
    data = dfs[0]
    
    data = data[data['Attendance'] != 'Attendance']
    data = data[['Date', 'Unnamed: 4', 'Opp' ,'Rank', 'GB', 'D/N', 'Attendance']]
    data.rename(columns={'Unnamed: 4': 'HA'}, errors='ignore', inplace=True)
    data['HA'].fillna('H', inplace=True)

    data['GB'] = data['GB'].str.replace('Tied', '0.0').str.replace('up ', '-')
    data['GB'] = data['GB'].astype(float)
    
    df = pd.concat([df, data], axis=0)
    
    df['Rank'] = df['Rank'].shift(1)
    df['GB'] = df['GB'].shift(1)
    df = df[1:]
 
    return df
