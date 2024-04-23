import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder



def preprocessing_data(filename:str):
    df = pd.read_excel(filename)
    # select only data with correlation under 0.79
    df = df[['spesies', 'color', 'hair cross section in the tip', 'medulla cross section in the tip', 'd medula', 'index medula']]
    # data cleaning for value "black, without gradation" and "black without gradation"
    df['color'] = df['color'].str.replace(',', '')
    # standarization of data
    df = standarization(df)
    # transform categorical data to numeric
    df = transform_to_numeric(df)
    return df

def standarization(df:pd.DataFrame):
    scaler = StandardScaler()
    feature_to_scale = df[['d medula', 'index medula']]
    model = scaler.fit(feature_to_scale)
    scaled_feature = model.transform(feature_to_scale)
    # this below should be improved
    scaled_feature_df = pd.DataFrame(scaled_feature, columns=['d medula', 'index medula'])
    df['d medula'] = scaled_feature_df['d medula']
    df['index medula'] = scaled_feature_df['index medula']
    return df

def transform_to_numeric(df:pd.DataFrame):
    le = LabelEncoder()
    for col in df.columns:
        if df[col].dtypes == 'object':
            df[col] = le.fit_transform(df[col])
    return df



if __name__ == "__main__":
    st.title("C5.0")
    uploaded_file = st.file_uploader("Upload a New File", type="xlsx", accept_multiple_files=False)


    if uploaded_file is not None:
        df = preprocessing_data(uploaded_file)
        st.dataframe(df)
        