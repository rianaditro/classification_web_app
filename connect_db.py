import streamlit as st

conn = st.connection('mysql', type='sql')
df = conn.query('SELECT * FROM dummy')

st.write(df)