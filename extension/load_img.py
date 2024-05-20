import streamlit as st


@st.cache_data
def load_all_images():
    # hair image order: circular, oval, triangular
    hair_img = ['static/hair_circular.jpg', 'static/hair_oval.jpg', 'static/hair_triangular.jpg']
    # medula image order: circular, flower shape, no cavity, oval
    medula_img = ['static/medula_circular.jpg', 'static/medula_flower.jpg', 'static/medula_no_cavity.jpg', 'static/medula_oval.jpg']
    return hair_img, medula_img

def load_class_image():
    barbatus_image = ['static/barbatus_image.jpg', 'static/barbatus_range.jpg']
    scrofa_image = ['static/scrofa_image.jpg', 'static/scrofa_range.jpg']
    verrucosus_image = ['static/verrucosus_image.png', 'static/verrucosus_range.jpg']
    celebensis_image = ['static/celebensis_image.PNG', 'static/barbatus_range.jpg']
    return barbatus_image, scrofa_image, verrucosus_image, celebensis_image