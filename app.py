import streamlit as st
import pandas as pd
import pickle

from C45 import C45Classifier
from streamlit_image_select import image_select
from sklearn.model_selection import train_test_split



def preprocessing_data(filename:str) -> pd.DataFrame:
    df = pd.read_excel(filename)
    try:
        df = df[['spesies', 'color', 'hair cross section in the tip', 'medulla cross section in the tip', 'd medula', 'index medula']]
        return df
    except:
        st.error("This file does not have the following fields: spesies, color, hair cross section in the tip, medulla cross section in the tip, d medula, index medula")
        return None

def split_data(df:pd.DataFrame):
    y = df['spesies']
    X = df.drop('spesies', axis=1)

    train_x, test_x, train_y, test_y = train_test_split(X,y,test_size=0.2,stratify=y)
    return train_x, test_x, train_y, test_y

def training_model(df:pd.DataFrame):
    train_x, test_x, train_y, test_y = split_data(df)

    model = C45Classifier()
    model.fit(train_x, train_y)
    summary = model.summary()
    evaluate = model.evaluate(test_x, test_y)

    return model, summary, evaluate

# model = pickle.load(open("model-py-81.pkl","rb"))

def calculate(var):
    st.write("calculated")
    st.write(var)

def user_input():
    with st.form("user_input"):
        st.write("Input Data")
        img = image_select("Species", ["babi1.jpg", "babi2.jpg"])
        color = st.selectbox("color", options=["black at the base to the middle, broken white at the tip",
                                    "black without gradation",
                                    "black at the base, broken white at the middle, dark brown at the tip",
                                    "black at the base and dark brown at the tip",
                                    "red at the base and dark brown at the tip",
                                    "white at the base and light brown at the tip",
                                    "dark brown at the base and black at the tip"])
        hair_cross_tip = st.selectbox("hair cross in the tip", options=["circular", "triangular"])
        medula_cross_tip = st.selectbox("medulla cross in the tip", options=["flower shape", "circular", "oval"])
        d_medula = st.number_input("d medula")
        index_medula = st.number_input("index medula")

        submit_btn = st.form_submit_button("Submit")

        if submit_btn:
            st.image(img)
            st.write(calculate(d_medula))


if __name__ == "__main__":
    st.title("C5.0")
    uploaded_file = st.file_uploader("Upload a New File", type="xlsx", accept_multiple_files=False)
    # st.checkbox("Use the existing model", value=False)

    if uploaded_file is not None:
        df = preprocessing_data(uploaded_file)
        if df is not None:
            st.dataframe(df)

            model, summary, evaluate = training_model(df)
            st.write(summary)
            st.write(evaluate)
            st.write("Nice try")
        

    