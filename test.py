import streamlit as st
import pandas as pd

conn = st.experimental_connection('databulu', type='sql')


if __name__ == "__main__":
    df = conn.query("SELECT * FROM dummy")
    st.write(df)