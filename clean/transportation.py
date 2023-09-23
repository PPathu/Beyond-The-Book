import pandas as pd

# load in data
df = pd.read_csv("data/transportation.csv")

# drop unnamed cols
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

print(df)
