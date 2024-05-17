import streamlit as st

from st_pages import show_pages_from_config

from extension.load_img import load_all_images, load_class_image

show_pages_from_config()
st.set_page_config(page_title="Home", initial_sidebar_state="collapsed")

# hair image order: circular, oval, triangular
# medula image order: circular, flower shape, no cavity, oval
hair_img, medula_img = load_all_images()
hair_captions = ['Hair cross section in the base', 'Hair cross section in the middle', 'Hair cros section in the tip']
medula_captions = ['Medula cross section in the base', 'Medula cross section in the middle', 'Medula cross section in the tip']

barbatus_image = load_class_image()
barbatus_taksonomi = {'Kerajaan':'Animalia','Filum':'Chordata', 'Kelas':'Mammalia','Ordo':'Artiodactyla', 'Famili':'Suidae', 'Tribus':'Suini','Genus':'Sus', 'Spesies':'Sus Barbatus'}
barbatus_desc = "Babi berjenggot berukuran cukup besar; hewan jantan mencapai panjang tubuh 1520 mm, yang betina sedikit lebih kecil; tinggi bahunya hingga 90 cm dan beratnya mencapai 120 kg, meskipun kebanyakan antara 57–83 kg."
barbatus_hair = [hair_img[0], hair_img[1], hair_img[0]]
barbatus_medula = [medula_img[2], medula_img[2], medula_img[1]]


def template(details, image, hair_image, medula_image):
    with st.container(border=True):
        st.subheader("***Sus Barbatus***", anchor=False)
        col1, col2 = st.columns(2)
        with col1:
            st.image(image[0])
        with col2:
            st.write("Babi berjenggot berukuran cukup besar; hewan jantan mencapai panjang tubuh 1520 mm, yang betina sedikit lebih kecil; tinggi bahunya hingga 90 cm dan beratnya mencapai 120 kg, meskipun kebanyakan antara 57–83 kg.")
        st.write("Ciri-ciri:")
        barbatus_caption = ['Hair section in the base', 'Hair section in the middle', 'Hair section in the tip', 'Medula section in the base', 'Medula section in the middle', 'Medula section in the tip']
        img1, img2, img3 = st.columns(3)
        img1.image(hair_image[0], caption=barbatus_caption[0], width=200)
        img2.image(hair_image[1], caption=barbatus_caption[1], width=200)
        img3.image(hair_image[2], caption=barbatus_caption[2], width=200)
        
        img4, img5, img6 = st.columns(3)
        img4.image(medula_image[0], caption=barbatus_caption[3], width=200)
        img5.image(medula_image[1], caption=barbatus_caption[4], width=200)
        img6.image(medula_image[2], caption=barbatus_caption[5], width=200)
        col3, col4 = st.columns(2, gap="medium")
        with col3:
            st.json(barbatus_taksonomi)
        with col4:
            st.image(image[1])


if __name__ == "__main__":
    template(barbatus_desc, barbatus_image, barbatus_hair, barbatus_medula)