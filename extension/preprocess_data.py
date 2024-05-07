import pandas as pd

from sklearn.preprocessing import StandardScaler, LabelEncoder

# this accept a single column dataframe df['d rambut'] for example
def summary(df:pd.DataFrame):
    mean = df.mean()
    std = df.std()
    p25 = df.quantile(0.25)
    p50 = df.quantile(0.5)
    p75 = df.quantile(0.75)
    return [mean, std, p25, p50, p75]

def base_processing(df:pd.DataFrame):
    df['color'] = df['color'].str.replace(",","")
    # standarization
    data_to_scale = df[['d rambut', 'd medula', 'index medula']]

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_to_scale)
    df[['d rambut', 'd medula', 'index medula']] = scaled_data
    return df

def tree_processing(df:pd.DataFrame):
    tree_df = df.copy()
    rambut_summary = summary(df['d rambut'])
    medula_summary = summary(df['d medula'])
    index_summary = summary(df['index medula'])

    bins_d_rambut = [-float('inf'), rambut_summary[2], rambut_summary[3], rambut_summary[4], float('inf')]
    bins_d_medula = [-float('inf'), medula_summary[2], medula_summary[3], medula_summary[4], float('inf')]
    bins_index = [-float('inf'), index_summary[2], index_summary[3], index_summary[4], float('inf')]

    labels = ['under 25%', 'under 50%', 'under 75%', '75% above']
    # convert numerical to categorical
    tree_df['d rambut'] = pd.cut(tree_df['d rambut'], bins=bins_d_rambut, labels=labels, include_lowest=True)
    tree_df['d medula'] = pd.cut(tree_df['d medula'], bins=bins_d_medula, labels=labels, include_lowest=True)
    tree_df['index medula'] = pd.cut(tree_df['index medula'], bins=bins_index, labels=labels, include_lowest=True)

    return tree_df

def knn_processing(df:pd.DataFrame):
    knn_df = df.copy()
    le = LabelEncoder()
    for col in df.columns:
        if knn_df[col].dtypes == 'object':
            knn_df[col] = le.fit_transform(df[col])
    return knn_df

# this is the big function of pre-processing
def pre_processing(df:pd.DataFrame):
    df = base_processing(df)
    tree_df = tree_processing(df)
    knn_df = knn_processing(df)
    return df, tree_df, knn_df
