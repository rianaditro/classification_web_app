import streamlit as st
import pandas as pd

from sklearn.preprocessing import StandardScaler


if __name__ == "__main__":
    df = pd.read_excel('databulu.xlsx')
    df.dropna(how='all', axis=1, inplace=True)
    df['color'] = df['color'].str.replace(",","")
    ls = df.nunique().to_list()
    idx = [i for i in range(len(ls)) if ls[i] == 1]

    df.drop(df.columns[idx],axis=1, inplace=True)

    mean_rambut = df['d rambut'].mean()
    mean_medula = df['d medula'].mean()
    mean_index = df['index medula'].mean()

    std_rambut = df['d rambut'].std()
    std_medula = df['d medula'].std()
    std_index = df['index medula'].std()

    scaler = StandardScaler()
    data_to_scale = df[['d rambut', 'd medula', 'index medula']]
    scaled_data = scaler.fit_transform(data_to_scale)
    df[['d rambut', 'd medula', 'index medula']] = scaled_data
    
    # percentile
    rambut_pers = [df['d rambut'].quantile(0.25), df['d rambut'].quantile(0.5), df['d rambut'].quantile(0.75)]
    medula_pers = [df['d medula'].quantile(0.25), df['d medula'].quantile(0.5), df['d medula'].quantile(0.75)]
    index_pers = [df['index medula'].quantile(0.25), df['index medula'].quantile(0.5), df['index medula'].quantile(0.75)]

    summary = [{'column': 'd rambut',
                'mean': mean_rambut,
                'std': std_rambut,
                'pers_25_scaled': rambut_pers[0],
                'pers_50_scaled': rambut_pers[1],
                'pers_75_scaled': rambut_pers[2]},
                {'column': 'd medula',
                'mean': mean_medula,
                'std': std_medula,
                'pers_25_scaled': medula_pers[0],
                'pers_50_scaled': medula_pers[1],
                'pers_75_scaled': medula_pers[2]},
                {'column': 'index medula',
                'mean': mean_index,
                'std': std_index,
                'pers_25_scaled': index_pers[0],
                'pers_50_scaled': index_pers[1],
                'pers_75_scaled': index_pers[2]}]
    print(summary)
    summary_df = pd.DataFrame(summary)
    summary_df.to_sql('summary.sql')

