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
from st_pages import show_pages_from_config, hide_pages

from extension.preprocess_data import summary
from extension.convert_input import to_categoric, std_scaled
from extension.load_img import load_all_images


# initialize options value for captions
color_value = ['black at the base and dark brown at the tip', 'black at the base broken white at the middle dark brown at the tip', 'black at the base to the middle broken white at the tip', 'black without gradation', 'dark brown at the base and black at the tip', 'red at the base and dark brown at the tip', 'white at the base and light brown at the tip']
hair_base_value = ['circular', 'oval', 'triangular']
hair_middle_value = ['circular', 'oval', 'triangular']
hair_tip_value = ['circular', 'triangular']
medula_base_value = ['circular', 'flower shape', 'no cavity']
medula_middle_value = ['flower shape', 'no cavity', 'oval']
medula_tip_value = ['circular', 'flower shape', 'oval']

# hair image order: circular, oval, triangular
# medula image order: circular, flower shape, no cavity, oval
hair_image, medula_image = load_all_images()

# maintaining image order based on input
# hair tip image order: circular, triangular
hair_tip_image = [hair_image[0], hair_image[2]]
# medula tip image order: circular, flower shape, no cavity
medula_base_image = medula_image[:3]
# medula middle image order: flower shape, no cavity, oval
medula_middle_image = medula_image[1:4]
# medula tip image order: circular, flower shape, oval
medula_tip_image = [medula_image[0], medula_image[1], medula_image[3]]


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

def predict_main():
    predicted = None
    st.header("Create a Prediction", anchor=False)
    with st.form("user_input"):
        st.subheader("User Input", anchor=False)
        color_input = st.selectbox(label="Hair Color", options=color_value)
        hair_base_input = image_select(label="Hair cross section in the base",
                                       images=hair_image,
                                       captions=hair_base_value, 
                                       return_value="index"
                                       )
        hair_middle_input = image_select(label="Hair cross section in the middle",
                                         images=hair_image,
                                         captions=hair_middle_value, 
                                         return_value="index"
                                         )
        hair_tip_input = image_select(label="Hair cross section in the tip",
                                      images=hair_tip_image,
                                      captions=hair_tip_value,
                                      return_value="index"
                                      )
        medula_base_input = image_select(label="Medula cross section in the base", 
                                         images=medula_base_image,
                                         captions=medula_base_value, 
                                         return_value="index"
                                         )
        medula_middle_input = image_select(label="Medula cross section in the middle", 
                                           images=medula_middle_image,
                                           captions=medula_middle_value, 
                                           return_value="index"
                                           )
        medula_tip_input = image_select(label="Medula cross section in the tip", 
                                        images=medula_tip_image,
                                        captions=medula_tip_value, 
                                        return_value="index"
                                        )
        st.image('static/diameter.jpg', caption="DM: Diameter Medula, DR: Diameter Rambut, Index medula: DM/DR")
        d_rambut_input = st.number_input("Diameter rambut",step=0)
        d_medula_input = st.number_input("Diameter medula",step=0)
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
    # reading login credentials from yaml file
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'])
    
    # login form if not authenticated
    authenticator.login()

    if st.session_state["authentication_status"]:
        # get role for authorize page access
        current_user = st.session_state['username']
        current_role = config['credentials']['usernames'][current_user]['role']
        st.session_state["role"] = current_role

        authenticator.logout(location='sidebar', key='logout predict')
        show_pages_from_config()
        
        # hide pages based on role
        if st.session_state["role"] == 'mitra' or st.session_state["role"] == 'taksonom lapangan':
            hide_pages(['Custom Prediction Page', 'Train Model Page', 'User Management'])
        elif st.session_state["role"] == 'pengembang model':
            hide_pages(['User Management Page'])
        elif st.session_state['role'] == 'admin':
            hide_pages([''])
        else:
            # prevent direct access from URL
            st.warning("You don't have access to this page")
        # page without role restriction
        predict_main()

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')