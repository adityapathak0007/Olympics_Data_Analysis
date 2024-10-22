import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import gdown


# Google Drive file URLs
athlete_events_url = 'https://drive.google.com/uc?id=1WDMrZ0Steqk2lcbf9gYa70Iy8ub1Laxr'
region_df_url = 'https://drive.google.com/uc?id=11fbDnfL18kcPHX36p9aLz_opAqoYeK_s'

# Download and load CSV data
@st.cache_data
def load_data():
    # Download the CSV files
    gdown.download(athlete_events_url, 'athlete_events.csv', quiet=False)
    gdown.download(region_df_url, 'noc_regions.csv', quiet=False)

    try:
        # Load CSV data
        df = pd.read_csv('athlete_events.csv', sep=',', on_bad_lines='skip', encoding='utf-8')
        region_df = pd.read_csv('noc_regions.csv', sep=',', on_bad_lines='skip', encoding='utf-8')

        # Clean column names by stripping spaces and converting to lowercase
        df.columns = df.columns.str.strip().str.lower()
        region_df.columns = region_df.columns.str.strip().str.lower()

        # Debug: Print cleaned column names for verification
        st.write("Cleaned columns in athlete_events.csv:", df.columns)
        st.write("Cleaned columns in noc_regions.csv:", region_df.columns)

        # Show a preview of the first few rows
        st.write("Preview of athlete_events.csv:", df.head())
        st.write("Preview of noc_regions.csv:", region_df.head())

    except pd.errors.ParserError as e:
        st.error(f"Error reading the CSV file: {e}")
        st.stop()
    
    return df, region_df


# Preprocess function
def preprocess(df, region_df):
    # Ensure column names are consistent
    df.columns = df.columns.str.strip().str.lower()
    region_df.columns = region_df.columns.str.strip().str.lower()

    # List of required columns and handle missing columns
    required_columns = ['year', 'season', 'city', 'sport', 'event', 'name', 'noc', 'medal', 'age', 'sex', 'weight', 'height']

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Error: The following columns are missing in the dataset: {missing_columns}")
        st.stop()

    # Filter for Summer Olympics
    df = df[df['season'] == 'summer']

    # Merge with region data
    df = df.merge(region_df, on='noc', how='left')

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # One hot encoding for medals
    df = pd.concat([df, pd.get_dummies(df['medal'])], axis=1)

    return df


# Main code execution
df, region_df = load_data()
df = preprocess(df, region_df)



# Sidebar and Layout
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete Wise Analysis')
)

# Main header and layout
st.markdown("""
    <style>
    .main-title {
        font-family: Arial, sans-serif;
        font-size: 48px;
        color: #00274D; /* Navy Blue */
        font-weight: bold;
        margin-bottom: 40px;
    }
    .section-header {
        font-family: Arial, sans-serif;
        font-size: 30px;
        color: #0073E6; /* Bright Blue */
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .stat-header {
        font-family: Arial, sans-serif;
        font-size: 24px;
        color: #00274D; /* Navy Blue */
        font-weight: bold;
    }
    .stat-number {
        font-family: Arial, sans-serif;
        font-size: 28px;
        color: #FF8C00; /* Orange */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Medal Tally Section
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.markdown('<div class="main-title">Overall Medal Tally</div>', unsafe_allow_html=True)
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.markdown(f'<div class="main-title">Medal Tally in {selected_year} Olympics</div>', unsafe_allow_html=True)
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.markdown(f'<div class="main-title">{selected_country} Overall Performance</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="main-title">{selected_country} Performance in {selected_year} Olympics</div>',
                    unsafe_allow_html=True)

    st.table(medal_tally)

# Overall Analysis Section
if user_menu == 'Overall Analysis':
    editions = df['year'].unique().shape[0] - 1
    cities = df['city'].unique().shape[0]
    sports = df['sport'].unique().shape[0]
    events = df['event'].unique().shape[0]
    athletes = df['name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.markdown('<div class="main-title">Top Statistics</div>', unsafe_allow_html=True)

    # Using 3 columns for stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-header">Editions</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number">{editions}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-header">Hosts</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number">{cities}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-header">Sports</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number">{sports}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-header">Events</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number">{events}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-header">Nations</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number">{nations}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-header">Athletes</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number">{athletes}</div>', unsafe_allow_html=True)

    # Participating Nations over the Years
    st.markdown('<div class="section-header">Participating Nations Over Time</div>', unsafe_allow_html=True)
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region', title="Nations Participating Over the Years")
    st.plotly_chart(fig)

    # Events over time
    st.markdown('<div class="section-header">Events Over Time</div>', unsafe_allow_html=True)
    events_over_time = helper.data_over_time(df, 'event')
    fig = px.line(events_over_time, x='Edition', y='event', title="Events Over the Years")
    st.plotly_chart(fig)

    # Number of Events over Time (Every Sport) - Heatmap
    st.markdown('<div class="section-header">Number of Events over Time (Every Sport)</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(subset=['year', 'sport', 'event'])
    pivot_table = x.pivot_table(index='sport', columns='year', values='event', aggfunc='count').fillna(0).astype(int)
    sns.heatmap(pivot_table, annot=True, fmt="d", cmap="YlOrBr", linewidths=0.5, ax=ax)
    st.pyplot(fig)

    # Most Successful Athletes
    st.markdown('<div class="section-header">Most Successful Athletes</div>', unsafe_allow_html=True)
    sport_list = df['sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

# Country-Wise Analysis Section
if user_menu == 'Country-Wise Analysis':
    st.sidebar.title('Country-Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    st.markdown(f'<div class="main-title">{selected_country} Medal Tally over the Years</div>', unsafe_allow_html=True)
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal Count', title=f"{selected_country} Medal Count Over the Years")
    st.plotly_chart(fig)

    st.markdown(f'<div class="section-header">{selected_country} Excels in the Following Sports</div>',
                unsafe_allow_html=True)
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 16))
    sns.heatmap(pt, annot=True, cmap="YlOrBr", linewidths=0.5, ax=ax)
    st.pyplot(fig)

    st.markdown(f'<div class="section-header">Top 10 Athletes from {selected_country}</div>', unsafe_allow_html=True)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

# Athlete-Wise Analysis Section
if user_menu == 'Athlete Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    st.markdown('<div class="section-header">Distribution of Age</div>', unsafe_allow_html=True)
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    st.markdown('<div class="section-header">Distribution of Age with Respect to Sports (Gold Medalists)</div>',
                unsafe_allow_html=True)
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing',
                     'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing',
                     'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball',
                     'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics',
                     'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    st.markdown('<div class="section-header">Height Vs Weight</div>', unsafe_allow_html=True)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', palette='deep', ax=ax)
    st.pyplot(fig)

    st.markdown('<div class="section-header">Men vs Women Participation Over the Years</div>', unsafe_allow_html=True)
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=["Male", "Female"], title="Men vs Women Participation Over the Years")
    st.plotly_chart(fig)
