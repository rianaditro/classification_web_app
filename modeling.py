import streamlit as st
import pandas as pd
import time
import pickle

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier  
from sklearn.metrics import accuracy_score
from C45 import C45Classifier

from preprocess_data import pre_processing


def model_training(dataset, model):
    y = dataset['spesies']
    X = dataset.drop(['spesies'], axis=1)

    # split data into train:test 80:20
    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2, stratify=y)
    # model training
    model.fit(train_x, train_y)
    # evaluate model
    prediction = model.predict(test_x)
    accuracy = accuracy_score(test_y, prediction)
    return model, accuracy

def main(df):
    df, tree_df, knn_df = pre_processing(df)
    tree = C45Classifier()
    knn = KNeighborsClassifier()
    tree_model, tree_acc = model_training(tree_df, tree)
    knn_model, knn_acc = model_training(knn_df, knn)
    return tree_model, tree_acc, knn_model, knn_acc

def save_model(model, filename):
    with open(f'db/{filename}.pkl', 'wb') as f:
        pickle.dump(model, f)


st.write('Create C5.0 and KNN model')
file_upload = st.file_uploader('Choose file', type=['xlsx'])
if file_upload is not None:
    df = pd.read_excel(file_upload)
    try:
        df = df[['spesies', 'color', 'hair cross section in the base', 'hair cross section in the middle', 'hair cross section in the tip', 'medulla cross section in the base', 'medulla cross section in the middle', 'medulla cross section in the tip', 'd rambut', 'd medula', 'index medula']]
        st.write('Preview')
        st.dataframe(df.head())

        submit_btn = st.button('Confirm')
        if submit_btn:
            with st.status("Training models...", expanded=True) as status:
                st.write("Pre-processing...")
                time.sleep(2)
                st.write("Fitting the model...")
                time.sleep(1)
                st.write("Evaluating the model...")
                time.sleep(1)
                status.update(label="Finished.", expanded=False)
                
            tree_model, tree_acc, knn_model, knn_acc = main(df)
            st.write(f"C5.0 accuracy: {tree_acc}")
            st.write(f"KNN accuracy: {knn_acc}")
            save_model(tree_model, 'tree_web')
            save_model(knn_model, 'knn_web')

    except KeyError:
        st.warning("The uploaded file doesn't have the following column: 'spesies', 'color', 'hair cross section in the base', 'hair cross section in the middle', 'hair cross section in the tip', 'medulla cross section in the base', 'medulla cross section in the middle', 'medulla cross section in the tip', 'd rambut', 'd medula', 'index medula'.")
    except ValueError:
        st.warning("Sorry, we only accept files in .xlsx format.")
    