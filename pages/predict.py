import streamlit as st
import pandas as pd
import pickle

from C45 import C45Classifier

# reading model
with open("db/tree_model.pkl", "rb") as f:
        tree = pickle.load(f)


if __name__ == "__main__":
    predicted = None
    with st.form("user_input"):
        st.write("Input Data")
        color = st.selectbox("color", options=["black at the base to the middle broken white at the tip",
                                    "black without gradation",
                                    "black at the base broken white at the middle dark brown at the tip",
                                    "black at the base and dark brown at the tip",
                                    "red at the base and dark brown at the tip",
                                    "white at the base and light brown at the tip",
                                    "dark brown at the base and black at the tip"])
        hair_base = st.selectbox("hair cross section in the base", options=["circular", "oval", "triangular"])
        hair_middle = st.selectbox("hair cross section in the middle", options=["circular", "oval", "triangular"])
        hair_tip = st.selectbox("hair cross section in the tip", options=["circular", "triangular"])
        medula_base = st.selectbox("medulla cross section in the base", options=['circular', 'flower shape', 'no cavity'])
        medula_middle = st.selectbox("medulla cross section in the middle", options=['flower shape', 'no cavity', 'oval'])
        medula_tip = st.selectbox("medulla cross section in the tip", options=['circular', 'flower shape', 'oval'])
        # d_rambut = st.number_input("d rambut")
        # d_medula = st.number_input("d medula")
        # index_medula = st.number_input("index medula")
        d_rambut = st.selectbox("d rambut cat", options=["under 25%", "under 50%", "under 75%", "above 75%"])
        d_medula = st.selectbox("d medula cat", options=["under 25%", "under 50%", "under 75%", "above 75%"])
        index_medula = st.selectbox("index medula cat", options=["under 25%", "under 50%", "under 75%", "above 75%"])

        user_input = [{'color': color,
                    'hair cross section in the base': hair_base,
                    'hair cross section in the middle': hair_middle,
                    'hair cross section in the tip': hair_tip,
                    'medulla cross section in the base': medula_base,
                    'medulla cross section in the middle': medula_middle,
                    'medulla cross section in the tip': medula_tip,
                    'd rambut cat': d_rambut,
                    'd medula cat': d_medula,
                    'index medula cat': index_medula}]
        
        submit_btn = st.form_submit_button("Submit")

        if submit_btn:
            predicted = tree.predict(user_input)[0]

    if predicted is not None:
         st.write(predicted)