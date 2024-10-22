import pandas as pd
import numpy as np

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['team', 'noc', 'games', 'year', 'city', 'sport', 'event', 'medal'])
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

    # If looking for a specific country, group by 'year', otherwise group by 'region'
    if flag == 1:
        x = temp_df.groupby('year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    # Calculate total medals
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # Display the result
    return x


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['team', 'noc', 'games', 'year', 'city', 'sport', 'event', 'medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                     ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df, col):
    nations_over_time = (
        df.drop_duplicates(['year', col])  # Keep unique (Year, region) pairs
        .groupby('Year')  # Group by Year
        .size()  # Get the size (count) of each group
        .reset_index(name= 'counts')  # Reset index and name the count column
        .sort_values('year')  # Sort by Year
    )
    nations_over_time.rename(columns={'year': 'Edition', 'counts': col}, inplace=True)
    return nations_over_time  # Correctly return the processed DataFrame


def most_successful(df, sport):
    # Consider only rows where a medal was awarded
    temp_df = df.dropna(subset=['medal'])

    # Filter by sport if specified
    if sport != 'Overall':
        temp_df = temp_df[temp_df['sport'] == sport]

    # Count medals for each athlete
    athlete_medal_count = temp_df['name'].value_counts().reset_index()
    athlete_medal_count.columns = ['name', 'Medal Count']  # Rename columns for clarity

    # Merge to add other details like sport, region, etc., avoiding duplication
    merged_df = athlete_medal_count.merge(df[['name', 'sport', 'region']], on='Name', how='left').drop_duplicates(
        'Name')

    return merged_df.head(15)


def yearwise_medal_tally(df, country):
    # Consider only rows where a medal was awarded
    temp_df = df.dropna(subset=['medal'])
    # Remove duplicates to ensure each medal is counted only once
    temp_df.drop_duplicates(subset=['team', 'noc', 'games', 'year', 'city', 'sport', 'event', 'medal'], inplace=True)
    # Group by region (country) and Year, then count the medals
    medal_tally = temp_df.groupby(['region', 'year']).count()['medal'].reset_index()
    # Rename columns for clarity
    medal_tally.columns = ['country', 'year', 'medal count']
    # Replace 'YourCountryName' with the specific country you want to filter for
    specific_country = country
    country_medal_tally = medal_tally[medal_tally['country'] == specific_country]
    return country_medal_tally


def country_event_heatmap(df, country):
    # Consider only rows where a medal was awarded
    temp_df = df.dropna(subset=['medal'])
    # Remove duplicates to ensure each medal is counted only once
    temp_df.drop_duplicates(subset=['team', 'noc', 'games', 'year', 'city', 'sport', 'event', 'medal'], inplace=True)

    # Filter for the specific country
    country_df = temp_df[temp_df['region'] == country]

    # Check if the filtered DataFrame is empty
    if country_df.empty:
        # Get unique sports and years from the original DataFrame
        unique_sports = df['sport'].unique()
        unique_years = df['year'].unique()

        # Create a DataFrame filled with zeros
        heatmap_data = pd.DataFrame(0, index=unique_sports, columns=unique_years)
        return heatmap_data

    # Count medals by sport and year for the specific country
    sport_yearly_medal_count = country_df.groupby(['Sport', 'Year']).count()['Medal'].reset_index()

    # Rename columns for clarity
    sport_yearly_medal_count.columns = ['Sport', 'Year', 'Medal Count']

    # Create a pivot table
    heatmap_data = sport_yearly_medal_count.pivot_table(index='Sport', columns='Year', values='Medal Count',
                                                        fill_value=0)
    return heatmap_data


def most_successful_countrywise(df, country):
    # Consider only rows where a medal was awarded
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    # Count medals for each athlete
    athlete_medal_count = temp_df['Name'].value_counts().reset_index()
    athlete_medal_count.columns = ['Name', 'Medal Count']  # Rename columns for clarity

    # Merge to add other details like sport, region, etc., avoiding duplication
    merged_df = athlete_medal_count.merge(df[['Name', 'Sport']], on='Name', how='left').drop_duplicates(
        'Name')

    return merged_df.head(10)


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else :
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.fillna(0, inplace=True)
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final
