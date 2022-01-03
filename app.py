import pandas as pd
import streamlit as st
import preprocess, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
df_region = pd.read_csv('noc_regions.csv')

df = preprocess.preprocess(df, df_region)

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)


if user_menu == 'Medal Tally':
    years, country = helper.country_year(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally = helper.fetch_metal_tally(df, selected_year, selected_country)

    if selected_year == 'overall' and selected_country == 'overall':
        st.title('Overall Tally')
    if selected_year != 'overall' and selected_country == 'overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'overall' and selected_country!='overall':
        st.title(selected_country + ' overall Olympics performance')
    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country + ' performance in '+str(selected_year) + ' Olympics')

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1 #Since 1906 event doesn't count as olympic event
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)

    with col2:
        st.header('Countries')
        st.title(nations)

    with col3:
        st.header('Athletes')
        st.title(athletes)

    participant_countries = helper.participant_nations_over_year(df)
    fig = px.line(participant_countries, x='Edition', y='num_of_participant')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)

    event_vis = helper.event_vis(df, 'Event')
    fig = px.line(event_vis, x='Edition', y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)

    st.title('Number of Events Per Editions')
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot = True)
    st.pyplot(fig)

    st.title('Most successful athelets')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    df_country = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(df_country, x='Year', y='Medal')
    st.title(selected_country +' Medal Tally over the year')
    st.plotly_chart(fig)

    st.title(selected_country + ' excels in the following sports')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title('Top 10 athletes of ' + selected_country)
    top10_athletes = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_athletes)

if user_menu == 'Athlete-wise Analysis':
    st.title('Distribution of Age')
    df_athletes = df.drop_duplicates(subset=['Name', 'region'])
    x1 = df_athletes['Age'].dropna()
    x2 = df_athletes[df_athletes['Medal'] == 'Gold']['Age'].dropna()
    x3 = df_athletes[df_athletes['Medal'] == 'Silver']['Age'].dropna()
    x4 = df_athletes[df_athletes['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=960, height=600)
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title('Height vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title('Men vs Women Participation over the year')
    final = helper.men_v_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=960, height=600)
    st.plotly_chart(fig)

