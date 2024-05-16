import streamlit as st
import pandas as pd
import pickle
import streamlit_authenticator as stauth
import yaml

from yaml.loader import SafeLoader
from st_pages import show_pages_from_config, hide_pages

from extension.preprocess_data import summary
from pages.predict import predict_main as predict_page


def save_model(model, filename):
    with open(f'db/{filename}.pkl', 'wb') as f:
        pickle.dump(model, f)

def main():
    st.header("Custom Prediction Page", anchor=False)
    with st.container(border=True):
        st.subheader("Upload files", anchor=False)
        dataset_upload = st.file_uploader('Choose file for dataset training', type=['xlsx'])
        tree_model_upload = st.file_uploader('Choose file for C5 model', type=['pkl'])
        knn_model_upload = st.file_uploader('Choose file for KNN model', type=['pkl'])

    if dataset_upload and tree_model_upload and knn_model_upload:
        df = pd.read_excel(dataset_upload)
        rambut_summary = summary(df['d rambut'])
        medula_summary = summary(df['d medula'])
        index_summary = summary(df['index medula'])

        # reading uploaded model
        tree_model = pickle.load(tree_model_upload)

        knn_model = pickle.load(knn_model_upload)
        
        predict_page()

        # Confirm before replace the current model
        with st.popover("Set as default model"):
            st.write("Do you want to replace the current model with the updated model?")
            set_def = st.button("Confirm")
            if set_def:
                save_model(tree_model, 'default_tree_model')
                save_model(knn_model, 'default_knn_model')
                df.to_excel('db/uploaded_file.xlsx', index=False)

                st.session_state.success = True


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

        authenticator.logout(location='sidebar')
        show_pages_from_config()
        
        # hide pages based on role: only admin and pengembang model can access
        if st.session_state["role"] == 'pengembang model':
            hide_pages(['User Management Page'])
            main()
        elif st.session_state['role'] == 'admin':
            hide_pages([])
            main()
        else:
            # prevent direct access from URL
            st.warning("You don't have access to this page")
            authenticator.logout(location='sidebar')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
