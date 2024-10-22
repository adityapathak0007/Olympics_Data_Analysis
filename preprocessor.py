import pandas as pd
import numpy as np

def preprocess(df, region_df):
    # Check if 'Season' column exists
    if 'Season' not in df.columns:
        raise KeyError("The DataFrame does not contain the 'Season' column.")

    # Filtering for summer olympics
    df = df[df['Season'] == 'Summer']

    # Merge with region_df
    df = df.merge(region_df, on='NOC', how='left')

    # Dropping duplicates
    df.drop_duplicates(inplace=True)

    # One hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    
    return df
