import streamlit as st
import pandas as pd
from sqlalchemy.sql import text
from sqlalchemy import create_engine


conn = st.connection('mysql', type='sql')
cursor = conn._connect()

with conn.session as s:
    st.markdown(f"Note that `s` is a `{type(s)}`")
    summ = pd.read_excel('db/clean_data_bulu.xlsx')
    summ.to_sql('dataset', cursor, if_exists='replace')

    # ins = text("CREATE TABLE IF NOT EXISTS pet_owners (person TEXT, pet TEXT)")
    # s.execute(ins)
    # # s.execute(text('DELETE FROM pet_owners;'))
    # pet_owners = ['jerry', 'fish', 'barbara', 'cat', 'alex', 'puppy']
    # s.execute(text(f'INSERT INTO pet_owners (person, pet) VALUES ("{pet_owners[4]}", "{pet_owners[5]}")'))
    # s.commit()

pet_owners = conn.query('select * from dataset')
st.dataframe(pet_owners, hide_index=True)