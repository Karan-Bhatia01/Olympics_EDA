import streamlit as st
import pandas as pd 
import preprocessor, helper
import plotly.express as px
import plotly.figure_factory as ff  # For distplot
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessor import preprocess

# Load datasets
df = pd.read_csv("dataset/athlete_events.csv")
region_df = pd.read_csv("dataset/noc_regions.csv")

# Preprocess the data
df = preprocessor.preprocess(df, region_df)

# Sidebar and menu options
st.sidebar.title("Welcome To Olympics Analysis")
user_menu = st.sidebar.radio(
    "Select an Option",
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete Analysis')
)

# -----------------------------
# Medal Tally Section
# -----------------------------
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, countries = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance")
    else:
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")
        
    st.table(medal_tally)

# -----------------------------
# Overall Analysis Section
# -----------------------------
if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Editions", editions)
    col2.metric("Hosts", cities)
    col3.metric("Sports", sports)

    col1, col2, col3 = st.columns(3)
    col1.metric("Events", events)
    col2.metric("Nations", nations)
    col3.metric("Athletes", athletes)

    # Participating Nations over the years
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="Count", title="Participating Nations over the Years")
    st.plotly_chart(fig)

    # Events over the years
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Count", title="Events over the Years")
    st.plotly_chart(fig)

    # Athletes over the years
    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Count", title="Athletes over the Years")
    st.plotly_chart(fig)

    # Heatmap for No. of Events over time for every sport
    st.title("No. of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    heatmap_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    sns.heatmap(heatmap_data, annot=True, ax=ax)
    st.pyplot(fig)

    # Most successful Athletes
    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    top_athletes = helper.most_successful(df, selected_sport)
    st.table(top_athletes)

# -----------------------------
# Country-Wise Analysis Section
# -----------------------------
if user_menu == 'Country-Wise Analysis':
    st.sidebar.title('Country-Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    
    # Year-wise Medal Tally for the selected country
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal", title=f"{selected_country} Medal Tally Over the Years")
    st.plotly_chart(fig)
    
    # Heatmap for sports in which the country excels
    st.title(f"{selected_country} Excels in the Following Sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True, ax=ax)
    st.pyplot(fig)
    
    # Top 10 athletes of the selected country
    st.title(f"Top 10 Athletes of {selected_country}")
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

# -----------------------------
# Athlete Analysis Section
# -----------------------------
if user_menu == 'Athlete Analysis':
    st.title("Athlete Analysis")
    
    # Distribution of Age for different medalists using Plotly Figure Factory
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    
    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
        show_hist=False,
        show_rug=False
    )
    fig.update_layout(autosize=False, width=1000, height=600, title="Distribution of Age")
    st.plotly_chart(fig)
    
    # Distribution of Age with respect to selected sports (Gold Medalists)
    st.title("Distribution of Age wrt Sports (Gold Medalist)")
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    age_data = []
    sport_names = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        if not gold_ages.empty:
            age_data.append(gold_ages)
            sport_names.append(sport)
    
    if age_data:
        fig = ff.create_distplot(age_data, sport_names, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.plotly_chart(fig)
    else:
        st.write("No Gold Medalist age data available for the selected sports.")
    
    # Height vs Weight scatter plot for athletes
    st.title("Height Vs Weight")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60, ax=ax)
    ax.set_title("Height vs Weight")
    st.pyplot(fig)
    
    # Men vs Women Participation over the Years
    st.title("Men vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"], title="Men vs Women Participation")
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
