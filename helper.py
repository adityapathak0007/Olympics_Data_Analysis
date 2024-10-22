import pandas as pd
import numpy as np

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['noc', 'year', 'sport', 'event', 'medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['noc', 'year', 'sport', 'event', 'medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')

    return medal_tally


def country_year_list(df):
    years = df['year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df, col):
    nations_over_time = (
        df.drop_duplicates(['year', col])  # Keep unique (Year, region) pairs
        .groupby('year')  # Group by Year
        .size()  # Get the size (count) of each group
        .reset_index(name='counts')  # Reset index and name the count column
        .sort_values('year')  # Sort by Year
    )
    nations_over_time.rename(columns={'year': 'Edition', 'counts': col}, inplace=True)
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['sport'] == sport]

    athlete_medal_count = temp_df['name'].value_counts().reset_index()
    athlete_medal_count.columns = ['Name', 'Medal Count']

    merged_df = athlete_medal_count.merge(df[['name', 'sport', 'region']], on='Name', how='left').drop_duplicates('Name')
    return merged_df.head(15)


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['medal'])
    temp_df.drop_duplicates(subset=['noc', 'year', 'sport', 'event', 'medal'], inplace=True)
    medal_tally = temp_df.groupby(['region', 'year']).count()['medal'].reset_index()
    medal_tally.columns = ['Country', 'Year', 'Medal Count']

    country_medal_tally = medal_tally[medal_tally['Country'] == country]
    return country_medal_tally


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['medal'])
    temp_df.drop_duplicates(subset=['noc', 'year', 'sport', 'event', 'medal'], inplace=True)

    country_df = temp_df[temp_df['region'] == country]

    if country_df.empty:
        unique_sports = df['sport'].unique()
        unique_years = df['year'].unique()
        heatmap_data = pd.DataFrame(0, index=unique_sports, columns=unique_years)
        return heatmap_data

    sport_yearly_medal_count = country_df.groupby(['sport', 'year']).count()['medal'].reset_index()
    sport_yearly_medal_count.columns = ['Sport', 'Year', 'Medal Count']

    heatmap_data = sport_yearly_medal_count.pivot_table(index='Sport', columns='Year', values='Medal Count', fill_value=0)
    return heatmap_data


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['medal'])
    temp_df = temp_df[temp_df['region'] == country]

    athlete_medal_count = temp_df['name'].value_counts().reset_index()
    athlete_medal_count.columns = ['Name', 'Medal Count']

    merged_df = athlete_medal_count.merge(df[['name', 'sport']], on='Name', how='left').drop_duplicates('Name')
    return merged_df.head(10)


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['name', 'region'])
    athlete_df['medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['name', 'region'])
    men = athlete_df[athlete_df['sex'] == 'M'].groupby('year').count()['name'].reset_index()
    women = athlete_df[athlete_df['sex'] == 'F'].groupby('year').count()['name'].reset_index()
    final = men.merge(women, on='year', how='left')
    final.fillna(0, inplace=True)
    final.rename(columns={'name_x': 'Male', 'name_y': 'Female'}, inplace=True)
    return final
