import streamlit as st
import pandas as pd
import pickle

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier  
from sklearn.metrics import accuracy_score
from C45 import C45Classifier


# this for pre-processing data 
def mean_df(df):
    # the value should be updated to db
    mean_rambut = df['d rambut'].mean()
    mean_medula = df['d medula'].mean()
    mean_index = df['index medula'].mean()
    return [mean_rambut, mean_medula, mean_index]

def std_df(df):
    std_rambut = df['d rambut'].std()
    std_medula = df['d medula'].std()
    std_index = df['index medula'].std()
    return [std_rambut, std_medula, std_index]

def percentile(df):
    p_25 = [df['d rambut'].quantile(0.25), df['d medula'].quantile(0.25), df['index medula'].quantile(0.25)]
    p_50 = [df['d rambut'].quantile(0.5), df['d medula'].quantile(0.5), df['index medula'].quantile(0.5)]
    p_75 = [df['d rambut'].quantile(0.75), df['d medula'].quantile(0.75), df['index medula'].quantile(0.75)]
    return p_25, p_50, p_75

def base_processing(df):
    df['color'] = df['color'].str.replace(",","")
    # standarization
    data_to_scale = df[['d rambut', 'd medula', 'index medula']]

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_to_scale)
    df[['d rambut', 'd medula', 'index medula']] = scaled_data
    return df

def tree_processing(df):
    tree_df = df.copy()
    # check if it needs to change when using db
    bins_d_rambut = [-float('inf'), df['d rambut'].quantile(0.25), df['d rambut'].quantile(0.5), df['d rambut'].quantile(0.75), float('inf')]
    bins_d_medula = [-float('inf'), df['d medula'].quantile(0.25), df['d medula'].quantile(0.5), df['d medula'].quantile(0.75), float('inf')]
    bins_index = [-float('inf'), df['index medula'].quantile(0.25), df['index medula'].quantile(0.5), df['index medula'].quantile(0.75), float('inf')]

    labels = ['under 25%', 'under 50%', 'under 75%', '75% above']
    # convert numerical to categorical
    tree_df['d rambut'] = pd.cut(tree_df['d rambut'], bins=bins_d_rambut, labels=labels, include_lowest=True)
    tree_df['d medula'] = pd.cut(tree_df['d medula'], bins=bins_d_medula, labels=labels, include_lowest=True)
    tree_df['index medula'] = pd.cut(tree_df['index medula'], bins=bins_index, labels=labels, include_lowest=True)

    return tree_df

def knn_processing(df):
    knn_df = df.copy()
    le = LabelEncoder()
    for col in df.columns:
        if knn_df[col].dtypes == 'object':
            knn_df[col] = le.fit_transform(df[col])
    return knn_df

# this is the big function of pre-processing
def pre_processing(df):
    df = base_processing(df)
    tree_df = tree_processing(df)
    knn_df = knn_processing(df)
    return df, tree_df, knn_df

# this is the processing for modelling
def data_training(dataset, model):
    y = dataset['spesies']
    X = dataset.drop(['spesies'], axis=1)

    # split data into train:test 80:20
    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2, stratify=y)
    # model training
    model.fit(train_x, train_y)
    # evaluate model
    prediction = model.predict(test_x)
    accuracy = accuracy_score(test_y, prediction)
    accuracy = "{:.2%}".format(accuracy)
    return model, accuracy

# this is the big function of modelling
def model_creation(df):
    df, tree_df, knn_df = pre_processing(df)
    tree = C45Classifier()
    knn = KNeighborsClassifier()
    tree_model, tree_acc = data_training(tree_df, tree)
    knn_model, knn_acc = data_training(knn_df, knn)
    return tree_model, tree_acc, knn_model, knn_acc
