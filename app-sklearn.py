import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier  
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


conn = st.experimental_connection('databulu', type='sql')

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

def main_pipeline(df:pd.DataFrame):
    # split data
    X = df.drop('spesies', axis=1)
    y = df['spesies']
    # cross validation using 10 fold
    skf = StratifiedKFold(n_splits=10)

    tree_algorithm = tree.DecisionTreeClassifier(criterion='entropy')
    knn_algorithm = KNeighborsClassifier(n_neighbors=11)

    folds_result = []
    best_tree_model = None
    best_tree_accuracy = 0.0

    for train_index, test_index in skf.split(X,y):
        # split data
        X_train, X_test = X.loc[train_index], X.loc[test_index]
        y_train, y_test = y.loc[train_index], y.loc[test_index]
        # modeling
        tree_model, tree_acc = model_pipeline(tree_algorithm, X_train, X_test, y_train, y_test)
        
        folds_result.append(tree_acc)
        if tree_acc > best_tree_accuracy:
            best_tree_accuracy = tree_acc
            best_tree_model = tree_model
    return best_tree_model, best_tree_accuracy, folds_result


def model_pipeline(algorithm, X_train, X_test, y_train, y_test):
    model = algorithm.fit(X_train, y_train)
    prediction = model.predict(X_test)
    accuracy = accuracy_score(prediction, y_test)
    return model, accuracy

def write_result(accuracy, folds_result):
    col_names = [f'Fold {i}' for i in range(1,11)]
    folds_df = pd.DataFrame([folds_result], columns=col_names)
    mean = sum(folds_result)/len(folds_result)

    st.dataframe(folds_df, use_container_width=True, hide_index=True)
    st.write(f'Average accuracy: {mean}')
    st.write(f'Best model accuracy: {accuracy}')


if __name__ == "__main__":
    st.title("C5.0")
    uploaded_file = st.file_uploader("Upload a New File", type="xlsx", accept_multiple_files=False)


    if uploaded_file is not None:
        df = preprocessing_data(uploaded_file)

        st.dataframe(df)

        model, accuracy, folds_result = main_pipeline(df)

        if st.button('Create Model', type='primary'):
            write_result(accuracy, folds_result)
        