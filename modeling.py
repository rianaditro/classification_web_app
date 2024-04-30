import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier  
from sklearn.metrics import accuracy_score, confusion_matrix
from C45 import C45Classifier

from preprocess_data import pre_processing

# conn = st.experimental_connection('databulu', type='sql')

def tree_training(tree_df):
    y_tree = tree_df['spesies']
    X_tree = tree_df.drop(['spesies'], axis=1)

    train_x, test_x, train_y, test_y = train_test_split(X_tree, y_tree, test_size=0.2, stratify=y_tree)

    model = C45Classifier()
    model.fit(train_x, train_y)
    pred = model.predict(test_x)
    acc = accuracy_score(test_y, pred)
    return model, acc

def knn_training(knn_df):
    y_knn = knn_df['spesies']
    X_knn = knn_df.drop(['spesies'], axis=1)

    train_x, test_x, train_y, test_y = train_test_split(X_knn, y_knn, test_size=0.2, stratify=y_knn)

    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(train_x, train_y)
    pred = model.predict(test_x)
    acc = accuracy_score(test_y, pred)
    return model, acc

def main(df):
    df, tree_df, knn_df = pre_processing(df)
    tree_model, tree_acc = tree_training(tree_df)
    knn_model, knn_acc = knn_training(knn_df)
    return tree_model, tree_acc, knn_model, knn_acc


st.write('Create C5.0 and KNN model')
file_upload = st.file_uploader('Choose file')
if file_upload is not None:
    df = pd.read_excel(file_upload)
    try:
        df = df[['spesies', 'color', 'hair cross section in the base', 'hair cross section in the middle', 'hair cross section in the tip', 'medulla cross section in the base', 'medulla cross section in the middle', 'medulla cross section in the tip', 'd rambut', 'd medula', 'index medula']]
        st.write('Preview')
        st.dataframe(df.head())

        submit_btn = st.button('Confirm')
        if submit_btn:
            tree_model, tree_acc, knn_model, knn_acc = main(df)
            st.write(f"C5.0 accuracy: {tree_acc}")
            st.write(f"KNN accuracy: {knn_acc}")

    except KeyError:
        st.warning("The uploaded file doesn't have the following column: 'spesies', 'color', 'hair cross section in the base', 'hair cross section in the middle', 'hair cross section in the tip', 'medulla cross section in the base', 'medulla cross section in the middle', 'medulla cross section in the tip', 'd rambut', 'd medula', 'index medula'.")
    except ValueError:
        st.warning("Sorry, we only accept files in .xlsx format.")
    