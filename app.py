import streamlit as st
st.set_page_config(page_title="Home", initial_sidebar_state="collapsed")

import yaml
from yaml import SafeLoader
from st_pages import show_pages_from_config

from extension.load_img import load_all_images

show_pages_from_config()


hair_img, medula_img = load_all_images()

# load data from yaml file
with open('homepage_data.yaml') as f:
        data_list = yaml.load(f, Loader=SafeLoader)


def template(data:dict):
    with st.container(border=True):
        st.subheader(f"**{data['name']}** (*{data['class']}*)", anchor=False)
        st.image(data['image'], width=300)
        st.text_area("**Deskripsi**", data['description'], height=300)
        st.warning(f"Status Nasional: **{data['status']}**")
        if data['iucn'] == 'Vurnerable' or data['iucn'] == 'Endangered':
            st.error(f"Status IUCN: **{data['iucn']}**")
        else:
             st.warning(f"Status IUCN: **{data['iucn']}**")
        st.divider()
        st.write("**Ciri-ciri Morfologi Rambut**")
        st.image(data['hair']['main'], caption='Morfologi Rambut', use_column_width=True)
        hair_caption = ['Penampang melintang rambut bagian pangkal M:medulla', 
                        'Penampang melintang rambut bagian tengah M:medulla', 
                        'Penampang melintang rambut bagian ujung M:medulla']
        img1, img2, img3 = st.columns(3)
        img1.image(data['hair']['pangkal'], caption=hair_caption[0], width=200)
        img2.image(data['hair']['tengah'], caption=hair_caption[1], width=200)
        img3.image(data['hair']['ujung'], caption=hair_caption[2], width=200)
        st.divider()
        col3, col4 = st.columns(2, gap="medium")
        with col3:
            st.write("**Taksonomi**")
            t1, t2 = st.columns(2)
            for item in data['taksonom']:
                t1.write(f"**{item}**")
                t2.write(f"{data['taksonom'][item]}")
        with col4:
            st.image(data['map'], caption='Peta Persebaran', use_column_width=True)
        st.caption(f'Referensi: {data["source"]}')


if __name__ == "__main__":
    st.header("Home Page", anchor=False)
    for item in data_list:
        template(data_list[item])