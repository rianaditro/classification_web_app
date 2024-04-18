import streamlit as st
import pandas as pd
import pickle

from C45 import C45Classifier


df = pd.read_excel("databulu.xlsx")
model = pickle.load(open("model-py-81.pkl","rb"))

st.title("C5.0")
st.file_uploader("Upload a New File", type="xlsx")
st.checkbox("Use the existing model", value=False)

st.selectbox("color", options=["black at the base to the middle, broken white at the tip",
                               "black without gradation",
                               "black at the base, broken white at the middle, dark brown at the tip",
                               "black at the base and dark brown at the tip",
                               "red at the base and dark brown at the tip",
                               "white at the base and light brown at the tip",
                               "dark brown at the base and black at the tip"])
st.selectbox("hair cross in the tip", options=["circular", "triangular"])
st.selectbox("medulla cross in the tip", options=["flower shape", "circular", "oval"])
st.number_input("d medula")
st.number_input("index medula")