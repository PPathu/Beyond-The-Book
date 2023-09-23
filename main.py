import pandas as pd

from clean.transportation import clean_transportation

df = pd.read_csv("data/transportation.csv")
df = clean_transportation(df)
