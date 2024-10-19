# Functions for pre-processing the data
import pandas as pd
def one_hot(df,columns):
    df_encoded = pd.get_dummies(df[columns], drop_first=True)
    df_encoded = df_encoded.astype(int)
    df = pd.concat([df, df_encoded], axis=1)
    df.drop(columns=columns, inplace=True)  
    return df

def mapping_cols(df,columns):
    mapping = {'Yes' : 2, 'No':1, 'No internet service': 0, 'No phone service':0}
    for col in columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.strip().str.capitalize()
        df[col]=df[col].map(mapping)
    return df