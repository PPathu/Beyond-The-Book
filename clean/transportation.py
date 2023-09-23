import pandas as pd

def clean_transportation(df):
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['expense.transportation'] = df['expense.transportation'].str.replace(',', '').astype(float)
    return df

if __name__ == "__main__":
    # load in data
    df = pd.read_csv("data/transportation.csv", thousands=",")

    # drop unnamed cols
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]


