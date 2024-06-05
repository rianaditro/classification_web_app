import streamlit as st
import pandas as pd
import pickle
import streamlit_authenticator as stauth
import yaml, base64

from yaml.loader import SafeLoader
from st_pages import show_pages_from_config, hide_pages

from extension.preprocess_data import summary
from pages.predict import predict_main as predict_page


def save_model(model, filename):
    with open(f'db/{filename}.pkl', 'wb') as f:
        pickle.dump(model, f)

def validate_upload(dataframe_check):
    main_columns = ['spesies', 'color', 'hair cross section in the tip', 'hair cross section in the middle', 'hair cross section in the base', 'medulla cross section in the base', 'medulla cross section in the middle', 'medulla cross section in the tip', 'd rambut', 'd medula', 'index medula']

    if all(item in dataframe_check.columns for item in main_columns):
        return True, "Data Telah Sesuai."
    else:
        return False, f"Terdapat satu atau beberapa kolom yang tidak sesuai: {main_columns}"
    
def load_data(df:pd.DataFrame, tree_model_upload, knn_model_upload):
    rambut_summary = summary(df['d rambut'])
    medula_summary = summary(df['d medula'])
    index_summary = summary(df['index medula'])

    # reading uploaded model
    tree_model = pickle.load(tree_model_upload)
    knn_model = pickle.load(knn_model_upload)
    return rambut_summary, medula_summary, index_summary, tree_model, knn_model

def replace_model(df, tree_model, knn_model):
    st.write("Ganti model dengan model baru? Model lama akan terhapus.")
    set_def = st.button("Konfirmasi", key='confirm btn custom predict')
    if set_def:
        save_model(tree_model, 'default_tree_model')
        save_model(knn_model, 'default_knn_model')
        df.to_excel('db/uploaded_file.xlsx', index=False)

        st.session_state.success = True

def download_template():
    with open('static/template.xlsx', 'rb') as template:
        template = template.read()
        b64 = base64.b64encode(template)
        return st.markdown(f"<p>Unduh <a href='data:application/octet-stream;base64,{b64.decode()}' download='template.xlsx'>template</a> untuk menyesuaikan format data</p>", unsafe_allow_html=True)

def main():
    st.header("Sistem Identifikasi Rambut ***sus***", anchor=False)
    st.divider()
    st.subheader("Buat Prediksi Custom", anchor=False)
    dataset_upload = st.file_uploader('Pilih data training', type=['xlsx'])
    download_template()

    if dataset_upload:
        df = pd.read_excel(dataset_upload)
        validate, valid_message = validate_upload(df)
        if validate == False:
            st.error(valid_message)
        elif validate == True:
            tree_model_upload = st.file_uploader('Pilih file untuk model C5', type=['pkl'])
            knn_model_upload = st.file_uploader('Pilih file untuk model KNN', type=['pkl'])

            if tree_model_upload and knn_model_upload:        
                st.info(valid_message)
                # load data
                rambut_summary, medula_summary, index_summary, tree_model, knn_model = load_data(df, tree_model_upload, knn_model_upload)
                predict_page()
                # Confirm before replace the current model
                with st.popover("Set as default model"):
                    replace_model(df, tree_model, knn_model)


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

        authenticator.logout(location='sidebar', key='logout custom predict')
        show_pages_from_config()
        
        # hide pages based on role: only admin and pengembang model can access
        if st.session_state["role"] == 'pengembang model':
            hide_pages(['User Management'])
            main()
        elif st.session_state['role'] == 'admin':
            hide_pages([])
            main()
        else:
            # prevent direct access from URL
            st.warning("You don't have access to this page")
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
