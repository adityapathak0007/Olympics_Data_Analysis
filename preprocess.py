import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# Google Drive file URLs
athlete_events_url = 'https://drive.google.com/uc?id=11fbDnfL18kcPHX36p9aLz_opAqoYeK_s'
region_df_url = 'https://drive.google.com/uc?id=YOUR_REGION_CSV_FILE_ID'

# Download and load CSV data
@st.cache_data
def load_data():
    gdown.download(athlete_events_url, 'athlete_events.csv', quiet=False)
    gdown.download(region_df_url, 'noc_regions.csv', quiet=False)
    
    # Try loading with different configurations
    try:
        df = pd.read_csv('athlete_events.csv', sep=',', on_bad_lines='skip', encoding='utf-8')
        region_df = pd.read_csv('noc_regions.csv', sep=',', on_bad_lines='skip', encoding='utf-8')
    except pd.errors.ParserError:
        st.error("Error reading the CSV file. Please check the format.")
    
    return df, region_df

'''
print(df.head())
print(df.shape)
print(df.info())

print(region_df.head())
print(region_df.shape)
print(region_df.info())
'''

df = df[df['Season'] == 'Summer']
# print(df.head())
# print(df.shape)
# print(df.info())

#merging tow datasets on region to get country name from NOC
df = df.merge(region_df, on='NOC', how='left')
print(df.head())
print(df.shape)
print(df.info())

# checking for country names
print(df['region'].unique().shape)

# checking for null values and duplicate values
print(df.isnull().sum())
print(df.duplicated().sum())

# removing duplicate values
df.drop_duplicates(inplace=True)
# checking after removing
print(df.duplicated().sum())

# checking for medal values and creating separate column for each category
print(df['Medal'].value_counts())
print(pd.get_dummies(df['Medal']))

# horizontally concat two dataframes
df = pd.concat([df,pd.get_dummies(df['Medal'])], axis=1)
print(df.head())
print(df.shape)
print(df.info())

# this line giving medals on the basis of players participated so we have to remove duplicates
# print(df.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index())

medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
print(medal_tally.head())
print(medal_tally.shape)
print(medal_tally.info())

print(medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index())

medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
print("Medal Tally Total")
print(medal_tally['Total'])


years = df['Year'].unique().tolist()
years.sort()
print(years)
years.insert(0,'Overall')
print(years)

country = np.unique(df['region'].dropna().values).tolist()
country.sort()
print(country)
country.insert(0,'Overall')
print(country)

medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
print(medal_df[medal_df['region'] == 'India'])
print(medal_df[medal_df['Year'] == 2016])
print(medal_df[(medal_df['Year'] == 2016) & (medal_df['region'] == 'India')])


def fetch_medal_tally(year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    # If looking for a specific country, group by 'Year', otherwise group by 'region'
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    # Calculate total medals
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # Display the result
    print(x)

# Example function call
fetch_medal_tally(year='Overall', country='India')

# Overall Analysis
# 1. No. of Editions
# 2. No. of Cities
# 3. No. of Events/Sports
# 4. No. of Athletes
# 5. Participating Nations

print(df['Year'].unique())
print(df['Year'].unique().shape[0] - 1)
print(df['City'].unique())
print(df['City'].unique().shape)
print(df['Sport'].unique())
print(df['Sport'].unique().shape)
print(df['Event'].unique())
print(df['Event'].unique().shape)
print(df['Name'].unique())
print(df['Name'].unique().shape)
print(df['region'].unique())
print(df['region'].unique().shape)


nations_over_time = (
    df.drop_duplicates(['Year', 'region'])  # Keep unique (Year, region) pairs
    .groupby('Year')                        # Group by Year
    .size()                                 # Get the size (count) of each group
    .reset_index(name='counts')             # Reset index and name the count column
    .sort_values('Year')                    # Sort by Year
)
nations_over_time.rename(columns={'Year': 'Edition', 'counts': 'No. of Countries'}, inplace=True)
print(nations_over_time)

fig = px.line(nations_over_time, x='Edition', y='No. of Countries')
# fig.show()

nations_over_time = (
    df.drop_duplicates(['Year', 'Event'])
    .groupby('Year')
    .size()
    .reset_index(name='No. of Events')
    .sort_values('Year')
)
print(nations_over_time)


# Drop duplicates to ensure each Event-Sport-Year combination is unique
x = df.drop_duplicates(subset=['Year', 'Sport', 'Event'])

# Generate the pivot table for the number of unique events per sport per year
pivot_table = x.pivot_table(
    index='Sport',
    columns='Year',
    values='Event',  # Use 'Event' to count the number of unique events
    aggfunc='count'  # Count the number of unique events for each sport-year combination
).fillna(0).astype('int')  # Replace NaN values with 0 and cast to integers

# Increase figure size, remove annotations or adjust their font size
plt.figure(figsize=(18, 10))  # Increase figure size
sns.heatmap(
    pivot_table,
    annot=True,
    fmt="d",  # Format annotations as integers
    cmap="YlOrBr",  # Use a distinguishable color map
    linewidths=0.5,  # Add small gaps between the cells
    annot_kws={"size": 6}  # Adjust font size of annotations
)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate labels
plt.yticks(fontsize=8)  # Reduce font size of y-axis labels
# plt.show()


def most_successful(df, sport):
    # Consider only rows where a medal was awarded
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if specified
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals for each athlete
    athlete_medal_count = temp_df['Name'].value_counts().reset_index()
    athlete_medal_count.columns = ['Name', 'Medal Count']  # Rename columns for clarity

    # Merge to add other details like sport, region, etc., avoiding duplication
    merged_df = athlete_medal_count.merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates(
        'Name')

    return merged_df


# Example function call
print(most_successful(df, 'Gymnastics'))


# Country wise analysis
# 1. Country wise Medal tally per year(line plot)
# 2. Which Countries are good at which Sports heatmap
# 3. Most Successful Athletes(Top10)

# Consider only rows where a medal was awarded
temp_df = df.dropna(subset=['Medal'])
# Remove duplicates to ensure each medal is counted only once
temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
# Group by region (country) and Year, then count the medals
medal_tally = temp_df.groupby(['region', 'Year']).count()['Medal'].reset_index()
# Rename columns for clarity
medal_tally.columns = ['Country', 'Year', 'Medal Count']

# Display the result
print(medal_tally)


# Replace 'YourCountryName' with the specific country you want to filter for
specific_country = 'India'
country_medal_tally = medal_tally[medal_tally['Country'] == specific_country]

# Display the result for the specific country
print(country_medal_tally)

fig = px.line(country_medal_tally, x='Year', y='Medal Count')
# fig.show()




specific_country = 'UK'  # Example: India

# Consider only rows where a medal was awarded
temp_df = df.dropna(subset=['Medal'])

# Remove duplicates to ensure each medal is counted only once
temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

# Filter for the specific country
country_df = temp_df[temp_df['region'] == specific_country]

# Count medals by sport and year for the specific country
sport_yearly_medal_count = country_df.groupby(['Sport', 'Year']).count()['Medal'].reset_index()

# Rename columns for clarity
sport_yearly_medal_count.columns = ['Sport', 'Year', 'Medal Count']

# Create a pivot table
heatmap_data = sport_yearly_medal_count.pivot_table(index='Sport', columns='Year', values='Medal Count', fill_value=0)

# Create the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', cbar_kws={'label': 'Medal Count'})
plt.title(f'Heatmap of Medal Counts for {specific_country} by Sport and Year')
plt.xlabel('Year')
plt.ylabel('Sport')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
#plt.show()


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

    return merged_df


print(most_successful_countrywise(df,'Jamaica'))


athlete_df = df.drop_duplicates(subset=['Name', 'region'])

x1 = athlete_df['Age'].dropna()
x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

fig = ff.create_distplot([x1, x2, x3, x4],['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
# fig.show()
# print(athlete_df)

famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

x = []
name = []
for sport in famous_sports:
    temp_df = athlete_df[athlete_df['Sport'] == sport]
    x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
    name.append(sport)

fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
# fig.show()


# Fill NaN values in the 'Medal' column
athlete_df['Medal'].fillna('No Medal', inplace=True)

# Create a scatter plot of Weight vs. Height
plt.figure(figsize=(10, 6))
temp_df = athlete_df[athlete_df['Sport'] == 'Athletics']
sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', palette='deep')

# Add labels and title
plt.xlabel('Weight (kg)')
plt.ylabel('Height (cm)')
plt.title('Scatter Plot of Athlete Weight vs Height')
plt.legend(title='Medal Status')
#plt.show()


men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

final = men.merge(women, on='Year', how='left')
final.fillna(0, inplace=True)
final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
print(final)
fig= px.line(final, x='Year', y=["Male", "Female"])
fig.show()
