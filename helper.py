import numpy as np



def fetch_metal_tally(df, year, country):
    df_medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'City', 'Event', 'Medal'])
    flag = 0
    if year == 'overall' and country == 'overall':
        temp_df = df_medal_tally
    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = df_medal_tally[df_medal_tally['region'] == country]
    if year != 'overall' and country == 'overall':
        temp_df = df_medal_tally[df_medal_tally['Year'] == int(year)]
    if year != 'overall' and country != 'overall':
        temp_df = df_medal_tally[(df_medal_tally['region'] == country) & (df_medal_tally['Year'] == int(year))]

    if flag == 1:
        df_filtered = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        df_filtered = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()
    df_filtered['total'] = df_filtered['Gold'] + df_filtered['Silver'] + df_filtered['Bronze']

    df_filtered['Gold'] = df_filtered['Gold'].astype('int')
    df_filtered['Silver'] = df_filtered['Silver'].astype('int')
    df_filtered['Bronze'] = df_filtered['Bronze'].astype('int')
    df_filtered['total'] = df_filtered['total'].astype('int')

    return df_filtered

def participant_nations_over_year(df):
    df_participated_countries = df.drop_duplicates(['Year', 'region'])[
        'Year'].value_counts().reset_index().sort_values('index')
    df_participated_countries.rename(columns={'index': 'Edition', 'Year': 'num_of_participant'}, inplace = True)
    return df_participated_countries


def event_vis(df, col):
    df_event_vis = df.drop_duplicates(['Year', col])[
        'Year'].value_counts().reset_index().sort_values('index')
    df_event_vis.rename(columns={'index': 'Edition', 'Year': col}, inplace = True)
    return df_event_vis


def most_successful(df, sport):
    df_temp = df.dropna(subset = ['Medal'])
    if sport != 'Overall':
        df_temp = df_temp[df_temp['Sport']==sport]
    x = df_temp['Name'].value_counts().reset_index().head(15).merge(df,left_on='index', right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'}, inplace = True)
    return x



def medal_tally(df):
    df_medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'City', 'Event', 'Medal'])
    df_medal_tally = df_medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending = False).reset_index()
    df_medal_tally['total'] = df_medal_tally['Gold'] + df_medal_tally['Silver'] + df_medal_tally['Bronze']

    df_medal_tally['Gold'] = df_medal_tally['Gold'].astype('int')
    df_medal_tally['Silver'] = df_medal_tally['Silver'].astype('int')
    df_medal_tally['Bronze'] = df_medal_tally['Bronze'].astype('int')
    df_medal_tally['total'] = df_medal_tally['total'].astype('int')

    return df_medal_tally

def country_year(df):
    year = df.Year.unique().tolist()
    year.sort()
    year.insert(0, 'overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'overall')

    return  year, country

def yearwise_medal_tally(df, country):
    df_temp = df.dropna(subset=['Medal'])
    df_temp.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    df_new = df_temp[df_temp['region'] == country]
    df_final = df_new.groupby('Year').count()['Medal'].reset_index()

    return df_final

def country_event_heatmap(df,country):
    df_temp = df.dropna(subset=['Medal'])
    df_temp.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    df_new = df_temp[df_temp['region'] == country]

    pt = df_new.pivot_table(index='Sport',columns='Year',values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    df_temp = df.dropna(subset = ['Medal'])

    df_temp = df_temp[df_temp['region']==country]
    x = df_temp['Name'].value_counts().reset_index().head(15).merge(df,left_on='index', right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'}, inplace=True)
    return x

def weight_v_height(df, sport):
    df_athletes = df.drop_duplicates(subset=['Name', 'region'])
    df_athletes['Medal'].fillna('No Medal', inplace=True)
    if sport!='Overall':
        temp_df = df_athletes[df_athletes['Sport'] == sport]
        return temp_df
    else: return df_athletes

def men_v_women(df):
    df_athletes = df.drop_duplicates(subset=['Name', 'region'])
    men = df_athletes[df_athletes['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = df_athletes[df_athletes['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final