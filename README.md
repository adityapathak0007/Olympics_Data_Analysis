# Olympics Data Analysis 🏅

[View Olympics Data Analysis](https://olympicsdataanalysis-x8acfzimgrbjf2jgnltydy.streamlit.app/)

## Overview

The Olympics Data Analysis is a web application built using Streamlit. It provides insights and visualizations based on Olympic athlete data, allowing users to analyze medal tallies, overall statistics, country-wise performance, and athlete demographics.

## Features

- **Medal Tally:** 📊 View medal counts for specific years and countries.
- **Overall Analysis:** 📈 Analyze overall statistics, including editions, host cities, sports, events, athletes, and participating nations over the years.
- **Country-Wise Analysis:** 🌍 Dive into the performance of individual countries and their medal counts.
- **Athlete-Wise Analysis:** 👤 Explore athlete demographics, including age distribution, height vs. weight, and gender participation over the years.

## Technologies Used

- **Python:** 🐍 Programming language used for developing the app.
- **Streamlit:** 📈 Framework used for building the interactive web application.
- **Pandas:** 🗂️ Library used for data manipulation and analysis.
- **Plotly & Seaborn:** 📊 Libraries used for data visualization.
- **Matplotlib:** 🎨 Library for creating static, animated, and interactive visualizations in Python.
- **gdown:** 📥 Library for downloading files from Google Drive.

## Data Preprocessing Functions

The data preprocessing is handled by the `preprocessor` module, which includes the following functions:

### `preprocess(df, region_df)`
- **Purpose:** Cleans and prepares the athlete events DataFrame for analysis.
- **Functionality:**
  - Filters for Summer Olympics.
  - Merges with region DataFrame to include country names.
  - Removes duplicate entries.
  - One-hot encodes the `Medal` column for analysis.

## Helper Functions

The `helper` module contains various functions to aid in data analysis:

### `fetch_medal_tally(df, year, country)`
- **Purpose:** Fetches the medal tally for a specific year and country.
  
### `medal_tally(df)`
- **Purpose:** Calculates the overall medal tally for all countries.

### `country_year_list(df)`
- **Purpose:** Provides lists of unique years and countries for dropdown selections.

### `data_over_time(df, col)`
- **Purpose:** Analyzes the number of participating nations or events over time.

### `most_successful(df, sport)`
- **Purpose:** Returns the most successful athletes based on medal counts, filtered by sport if specified.

### `yearwise_medal_tally(df, country)`
- **Purpose:** Calculates the medal count for a specific country over the years.

### `country_event_heatmap(df, country)`
- **Purpose:** Generates a heatmap for the specific country’s performance across different sports over the years.

### `most_successful_countrywise(df, country)`
- **Purpose:** Returns the top 10 most successful athletes from a specified country.

### `weight_v_height(df, sport)`
- **Purpose:** Analyzes the height and weight distribution of athletes, with optional filtering by sport.

### `men_vs_women(df)`
- **Purpose:** Analyzes participation trends between male and female athletes over the years.

## How It Works

### Data Loading and Preprocessing

1. **Data Loading:**
   - 📥 The application downloads Olympic athlete data and region data from specified Google Drive links.

2. **Data Preprocessing:**
   - 🧹 The data is filtered for summer Olympics, merged with region information, and duplicates are removed.
   - 📊 One-hot encoding is applied to the Medal column for analysis.

### Analysis Sections

#### Medal Tally
- Allows users to select a year and country to view the medal tally.

#### Overall Analysis
- Displays top statistics and visualizes trends in participating nations and events over the years.

#### Country-Wise Analysis
- Users can select a country to view its medal tally and analyze its performance in different sports.

#### Athlete-Wise Analysis
- Provides insights into the distribution of athlete ages, height vs. weight relationships, and gender participation over time.

## Data Format
The app requires CSV files for athlete events and regions, which are automatically downloaded from Google Drive.

## View the App

You can view the live Olympics Data Analysis app by clicking on the link below:

[View Olympics Data Analysis](https://olympicsdataanalysis-x8acfzimgrbjf2jgnltydy.streamlit.app/)

## Contact

For any questions, suggestions, or feedback, please feel free to reach out:

- **Aditya Pathak** 👤
- **Email:** [adityapathak034@gmail.com](mailto:adityapathak034@gmail.com) 📧
- **GitHub:** [adityapathak0007](https://github.com/adityapathak0007) 🐙
- **LinkedIn:** [adityapathak07](https://www.linkedin.com/in/adityapathak07) 🔗

## Prerequisites

Ensure you have Python 3.7 or higher installed on your system.

## Clone the Repository

Clone the repository and install the required packages:

```bash
git clone https://github.com/adityapathak0007/Olympics_Data_Analysis
cd Olympics_Data_Analysis
pip install -r requirements.txt
