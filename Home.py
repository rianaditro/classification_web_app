import streamlit as st


with st.container(border=True):
    st.subheader("Sus Barbatus", anchor=False)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.image('assets/barbatus_image.jpg')
    with col2:
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")
    barbatus_img = ['assets/hair_circular.png', 'assets/hair_circular.png', 'assets/hair_triangular.png', 'assets/medula_circular.png', 'assets/medula_flower.png', 'assets/medula_oval.png']
    barbatus_caption = ['Hair section in the base', 'Hair section in the middle', 'Hair section in the tip', 'Medula section in the base', 'Medula section in the middle', 'Medula section in the tip']
    st.image(barbatus_img[:3], caption=barbatus_caption[:3], width=200)
    st.image(barbatus_img[3:], caption=barbatus_caption[3:], width=200)
    col3, col4 = st.columns(2, gap="medium")
    with col3:
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")
        st.write("some text here")
    with col4:
        st.image('assets/barbatus_range.png')