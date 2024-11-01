from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def histogram(df):
    # Create a histogram of the DataFrame
    df.hist()
    # Show the plot
    plt.show()


def boxplot(df):
    df.plot.box(subplots=True, sharey=False)
    plt.savefig('bp_example.png')
    plt.show()


def timeseries(df):
    df.plot(xlabel='start', ylabel='participants')
    plt.show()


def main():
    filepath = Path(__file__).parent.parent.joinpath('data',
    'paralympics_events_prepared.csv')
    dataframe = pd.read_csv(filepath)
    histogram(dataframe)
    boxplot(dataframe)
    timeseries(dataframe['start', 'participants'])


if __name__ == '__main__':
    main()
