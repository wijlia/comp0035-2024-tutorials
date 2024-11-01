from pathlib import Path
import pandas as pd

def describe_dataframe(csv_file_df):
    print(csv_file_df.describe())


def main():
    file_path_events = Path(__file__).parent.joinpath('data', 'paralympics_events_raw.csv')
    file_path_raw = Path(__file__).parent.joinpath('data', 'paralympics_all_raw.xlsx')

    pd.read_csv(file_path_events)
    pd.read_excel(file_path_raw)
    pd.read_excel(file_path_raw, "medal_standings")

    # Filepath of the csv data file
    try:
        file_path_raw = Path(__file__).parent.joinpath('data', 'paralympics_all_raw.xlsx')
    except FileNotFoundError as e:
        print(f"File not found. Please check the file path. Error: {e}")

    # Read the data from the file into a Pandas dataframe
    raw_df = pd.read_excel(file_path_raw, "medal_standings")
   
    # Call the function to describe the dataframe
    describe_dataframe(raw_df)



if __name__ == '__main__':
    main()
