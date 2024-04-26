import streamlit as st
import pandas as pd
import pickle

from C45 import C45Classifier


def mean_std(df_col):
    mean = df_col.mean()
    std = df_col.std()

    return mean, std

def scaled(num, mean, std):
    z = (num - mean) / std
    return z


if __name__ == "__main__":
    df = pd.read_excel('databulu.xlsx')
    summ = summary_value(df['d rambut'])
    print(summ)

# with st.form("user_input"):
#     st.write("Input Data")
#     color = st.selectbox("color", options=["black at the base to the middle broken white at the tip",
#                                 "black without gradation",
#                                 "black at the base broken white at the middle dark brown at the tip",
#                                 "black at the base and dark brown at the tip",
#                                 "red at the base and dark brown at the tip",
#                                 "white at the base and light brown at the tip",
#                                 "dark brown at the base and black at the tip"])
#     hair_cross_base = st.selectbox("hair cross section in the base", options=["circular", "triangular"])
#     d_rambut = st.number_input("d rambut")
#     d_medula = st.number_input("d medula")
#     index_medula = st.number_input("index medula")

#     submit_btn = st.form_submit_button("Submit")

#     if submit_btn:
#         st.write(color)
#         st.write(hair_cross_base)
#         st.write(d_rambut)
#         st.write(d_medula)
#         st.write(index_medula)