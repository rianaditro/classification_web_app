import streamlit as st
import pandas as pd
import pickle
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from C45 import C45Classifier
from sklearn.neighbors import KNeighborsClassifier
from collections import Counter
from streamlit_image_select import image_select

from extension.preprocess_data import summary
from extension.convert_input import to_categoric, std_scaled



# initialize options value
spesies_value = ['S. barbatus', 'S. celebensis', 'S. scofa', 'S. scrofa', 'S. verrucossus']
color_value = ['black at the base and dark brown at the tip', 'black at the base broken white at the middle dark brown at the tip', 'black at the base to the middle broken white at the tip', 'black without gradation', 'dark brown at the base and black at the tip', 'red at the base and dark brown at the tip', 'white at the base and light brown at the tip']
hair_base_value = ['circular', 'oval', 'triangular']
hair_middle_value = ['circular', 'oval', 'triangular']
hair_tip_value = ['circular', 'triangular']
medula_base_value = ['circular', 'flower shape', 'no cavity']
medula_middle_value = ['flower shape', 'no cavity', 'oval']
medula_tip_value = ['circular', 'flower shape', 'oval']

# image list
hair_image = ['assets/hair_circular.png', 'assets/hair_oval.png', 'assets/hair_triangular.png']
hair_tip_image = ['assets/hair_circular.png', 'assets/hair_triangular.png']
medula_base_image = ['assets/medula_circular.png', 'assets/medula_flower.png', 'assets/medula_no_cavity.png']
medula_middle_image = ['assets/medula_flower.png', 'assets/medula_no_cavity.png', 'assets/medula_oval.png']
medula_tip_image = ['assets/medula_circular.png', 'assets/medula_flower.png', 'assets/medula_oval.png']

# reading default model
with open("db/default_tree_model.pkl", "rb") as f:
        tree_model = pickle.load(f)

with open("db/default_knn_model.pkl", "rb") as f:
        knn_model = pickle.load(f)

# initialize data
df = pd.read_excel('db/uploaded_file.xlsx')
rambut_summary = summary(df['d rambut'])
medula_summary = summary(df['d medula'])
index_summary = summary(df['index medula'])


def knn_predict(user_input):
    distance, indices = knn_model.kneighbors(user_input)
    result = df['spesies'].iloc[indices[0]].to_list()
    counts = Counter(result)
    # 5 is the n of neighbors
    percentages = {key: count / 5 * 100 for key, count in counts.items()}

    return dict(sorted(percentages.items(), key=lambda item: item[1], reverse=True))

def main():
    predicted = None
    st.header("Create a Prediction", anchor=False)
    with st.form("user_input"):
        st.subheader("User Input", anchor=False)
        color_input = st.selectbox("Color", options=color_value)
        hair_base_input = 0
        hair_middle_input = 0
        hair_tip_input = 0
        # hair_base_input = image_select("Hair cross section in the base", hair_image, hair_base_value, return_value="index")
        # hair_middle_input = image_select("Hair cross section in the middle", hair_image, hair_middle_value, return_value="index")
        # hair_tip_input = image_select("Hair cross section in the tip", hair_tip_image, hair_tip_value, return_value="index")
        medula_base_input = image_select("Medula cross section in the base", medula_base_image, medula_base_value, return_value="index")
        medula_middle_input = image_select("Medula cross section in the middle", medula_middle_image, medula_middle_value, return_value="index")
        medula_tip_input = image_select("Medula cross section in the tip", medula_tip_image, medula_tip_value, return_value="index")
        st.image('assets/diameter.png', caption="DM: Diameter Medula, DR: Diameter Rambut, Index medula: DM/DR")
        d_rambut_input = st.number_input("d rambut",step=0)
        d_medula_input = st.number_input("d medula",step=0)
        index_medula_input = st.number_input("index medula",step=1e-7,format="%.6f")

        tree_input = [{'color': color_input,
                    'hair cross section in the base': hair_base_value[hair_base_input],
                    'hair cross section in the middle': hair_middle_value[hair_middle_input],
                    'hair cross section in the tip': hair_tip_value[hair_tip_input],
                    'medulla cross section in the base': medula_base_value[medula_base_input],
                    'medulla cross section in the middle': medula_base_value[medula_middle_input],
                    'medulla cross section in the tip': medula_tip_value[medula_tip_input],
                    'd rambut cat': to_categoric(d_rambut_input, rambut_summary),
                    'd medula cat': to_categoric(d_medula_input, medula_summary),
                    'index medula cat': to_categoric(index_medula_input, index_summary)}]
        
        knn_input = [[color_value.index(color_input), 
                      hair_base_input, 
                      hair_middle_input, 
                      hair_tip_input, 
                      medula_base_input, 
                      medula_middle_input, 
                      medula_tip_input, 
                      std_scaled(d_rambut_input, rambut_summary), 
                      std_scaled(d_medula_input, medula_summary), 
                      std_scaled(index_medula_input, index_summary)]]
        
        submit_btn = st.form_submit_button("Submit")

        if submit_btn:
            predicted = [tree_model.predict(tree_input)[0], knn_predict(knn_input)]

    if predicted is not None:
         with st.container(border=True):
            st.write("Hasil prediksi C5:")
            st.write(f"**{predicted[0]}**")
            st.write("Tingkat kemiripan dengan kelas lain:")

            for key, value in predicted[1].items():
                st.write(f"{key}: {value}%")


if __name__ == "__main__":
    # the authentication start here
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'])
    
    authenticator.login()

    if st.session_state["authentication_status"]:
        authenticator.logout(location='sidebar')
        main()
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')