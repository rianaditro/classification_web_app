import pandas as pd
import numpy as np


def basic_preprocessing(df):
    df.dropna(how='all', axis=1, inplace=True)
    df['color'] = df['color'].str.replace(",","")

    return df



if __name__ == "__main__":
    df = pd.read_excel('missing_databulu.xlsx')
    df['color'] = df['color'].str.replace(",","")

