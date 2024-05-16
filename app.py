import streamlit as st

from st_pages import show_pages_from_config

from extension.load_img import load_all_images

show_pages_from_config()
st.set_page_config(page_title="Home", initial_sidebar_state="collapsed")

# hair image order: circular, oval, triangular
# medula image order: circular, flower shape, no cavity, oval
hair_img, medula_img = load_all_images()



with st.container(border=True):
    st.subheader("Sus Barbatus", anchor=False)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.write("some text here")
        # st.image(barbatus_img[0])
    with col2:
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")

    barbatus_caption = ['Hair section in the base', 'Hair section in the middle', 'Hair section in the tip', 'Medula section in the base', 'Medula section in the middle', 'Medula section in the tip']
    st.image(hair_img, caption=barbatus_caption[:3], width=200)
    st.image(medula_img[:3], caption=barbatus_caption[3:], width=200)
    col3, col4 = st.columns(2, gap="medium")
    with col3:
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")
    with col4:
        # st.image(barbatus_img[1])
        st.write("some text here")