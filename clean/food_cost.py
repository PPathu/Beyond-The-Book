import pandas as pd

state_abbreviations = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

def clean_food_cost(df):
    df['cost'] = df['Average monthly cost of groceries per person']
    df['cost'] = df['cost'].replace('[\$,]', '', regex=True).astype(float)
    df.rename(columns={"State": "state"}, inplace=True)
    df['state'] = df['state'].map(state_abbreviations)
    df.drop(["Average monthly cost of groceries per person", "City analyzed (population)", "Rank"], axis=1, inplace=True)
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/food_cost_data.csv")
    df['cost'] = df['Average monthly cost of groceries per person']
    df['cost'] = df['cost'].replace('[\$,]', '', regex=True).astype(float)
    df.rename(columns={"State": "state"}, inplace=True)
    df['state'] = df['state'].map(state_abbreviations)
    df.drop(["Average monthly cost of groceries per person", "City analyzed (population)", "Rank"], axis=1, inplace=True)

    print(df.head())
