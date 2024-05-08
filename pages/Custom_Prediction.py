import streamlit as st
import pandas as pd
import pickle

from extension.preprocess_data import summary
from Create_a_Prediction import main


with st.container(border=True):
    st.markdown("**<span style='font-size:30px'>Upload file</span>**", unsafe_allow_html=True)
    dataset_upload = st.file_uploader('Choose file for dataset training', type=['xlsx'])
    tree_model_upload = st.file_uploader('Choose file for C5 model', type=['pkl'])
    knn_model_upload = st.file_uploader('Choose file for KNN model', type=['pkl'])

if dataset_upload and tree_model_upload and knn_model_upload:
    df = pd.read_excel(dataset_upload)
    rambut_summary = summary(df['d rambut'])
    medula_summary = summary(df['d medula'])
    index_summary = summary(df['index medula'])

    # reading uploaded model
    tree_model = pickle.load(tree_model_upload)

    knn_model = pickle.load(knn_model_upload)
    
    main()


