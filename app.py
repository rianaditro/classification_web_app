import streamlit as st
import pandas as pd
import pickle

from C45 import C45Classifier
from streamlit_image_select import image_select


df = pd.read_excel("databulu.xlsx")
model = pickle.load(open("model-py-81.pkl","rb"))

def calculate(var):
    st.write("calculated")
    st.write(var)

st.title("C5.0")
st.file_uploader("Upload a New File", type="xlsx")
st.checkbox("Use the existing model", value=False)

with st.form("user_input"):
    
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


