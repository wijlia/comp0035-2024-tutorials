from pathlib import Path
import pandas as pd

from tutorialpkg.mypkg2.mymodule2_2 import fetch_user_data
from tutorialpkg.mypkg2.mymodule2_1 import calculate_area_of_circle

mock_database = {
    1: {'name': 'Alice', 'email': 'alice@example.com', 'age': 30},
    42: {'name': 'Bob', 'email': 'bob@example.com', 'age': 45},
}

def main():
    # The functions are in the modules in mypkg2. You will need to import them.

    # Calculate the area of a circle with a radius of 10. Print the result.
    area = calculate_area_of_circle(10)
    print(f"The area is {area}.")

    # Use the fetch_user_data(user_id, database) function to print the data for the user with ID 42 that is in `mock_database` variable.
    print(fetch_user_data(42, mock_database))

    # Locate the data file `paralmpics_raw.csv` relative to this file using pathlib.Path. Prove it exists.

    # This script is located in a subfolder so you need to navigate up to the parent (src) and then its parent (project root), then down to the 'data' directory and finally the .csv file
    csv_file = Path(__file__).parent.parent.joinpath('data', 
    'paralympics_events_raw.csv')

    # Check if the file exists
    if csv_file.exists():
        print(f"CSV file found: {csv_file}")
    else:
        print("CSV file not found.")
    
    # Activity 2.03.1
    dataframe = pd.read_csv(csv_file)
    print(dataframe.shape)
    print(dataframe.head(n=5))
    print(dataframe.tail(n=5))
    print(dataframe.columns)
    print(dataframe.dtypes)
    print(dataframe.info())
    print(dataframe.describe())

    # Activity 2.04

    # Read the CSV file
    df = pd.read_csv(csv_file)
    columns_to_change = ['countries', 'events', 'participants_m', 
    'participants_f', 'participants']
    # Part of activity 2.07 (lines 49-52)
    df = df.drop(index=0)
    df = df.drop(index=17)
    df = df.drop(index=31)
    df=df.reset_index(drop=True)
    for column_name in columns_to_change:
        # Convert a specific column from float64 to int
     #   if df[column_name].dtypes == 'float64':
        df[column_name] = df[column_name].astype('int')
    
    print(df.loc[:, 'end'])
    print(df.loc[:, 'start'])
    df['start'] = pd.to_datetime(df['start'], format='%d/%m/%Y')
    df['end'] = pd.to_datetime(df['end'], format='%d/%m/%Y')

    # Activity 2.05
    npc_csv = Path(__file__).parent.parent.joinpath('data', 'npc_codes.csv')
    df_npc = pd.read_csv(npc_csv,  usecols=['Code', 'Name'], encoding='utf-8', encoding_errors='ignore')
    # Part of activity 2.07 (line 70-77)
    replacement_names = {
        'UK': 'Great Britain',
        'USA': 'United States of America',
        'Korea': 'Republic of Korea',
        'Russia': 'Russian Federation',
        'China': "People's Republic of China"}
    df.replace(to_replace=replacement_names)
    df_merged = df.merge(df_npc, how='left', left_on='country', right_on='Name')

    print(df_merged.loc[: ,['country', 'Code', 'Name']])

    # Activity 2.06
    df_prepared = df_merged.drop(columns=['URL', 'disabilities_included', 'highlights'], axis=1)
    print(df_prepared)

    # Activity 2.07
    # missing_rows = df_prepared[df.isna().any(axis=1)]
    # missing_columns = df_prepared[df.isna().any(axis=0)]
    df_prepared = df_prepared.drop(columns=['Name'], axis=1)

    # Activity 2.08
    print(df_prepared['type'].unique())
    df_prepared['type'] = df_prepared['type'].str.strip()
    df_prepared['type'] = df_prepared['type'].str.lower()
    print(df_prepared['type'])
    print(df_prepared['type'].unique())

    # Activity 2.09
    #df_merged['duration'] = df_merged['end'] - df_merged['start']
    df_prepared.insert(df_prepared.columns.get_loc('end'), 'duration', df_prepared['end'] - df_prepared['start'])
    df_prepared['duration'] = df_prepared['duration'].dt.days.astype(int)
    print(df_prepared['duration'])

    # Activity 2.10
    df_prepared.to_csv(index=False)


if __name__ == '__main__':
    main()