import pandas as pd

def preprocess(df, df_region):
    # consider only summer olympics
    df = df[df['Season'] == 'Summer']
    # two data set are merge based on 'NOC'
    df = df.merge(df_region, on='NOC', how='left')
    # dropping duplicate values
    df.drop_duplicates(inplace=True)
    # sep Medal column based on values
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df