import streamlit as st
import pandas as pd
import pickle
import time

from extension.modeling import model_creation


def save_model(model, filename):
    with open(f'db/{filename}.pkl', 'wb') as f:
        pickle.dump(model, f)

def download_model(filename, label):
    with open(filename, 'rb') as f:
        btn = st.download_button(label=label, data=f, file_name=filename)


# here is the start of the web component
st.write('Create C5.0 and KNN model')
file_upload = st.file_uploader('Choose file', type=['xlsx'], key='file_upload')

if 'success' not in st.session_state:
    st.caption("Upload your dataset file for model training.")
else:
    st.success('Model Updated.')

if file_upload is not None:
    df = pd.read_excel(file_upload)
    try:
        st.write('Preview')
        st.dataframe(df.head())

        df = df[['spesies', 'color', 'hair cross section in the base', 'hair cross section in the middle', 'hair cross section in the tip', 'medulla cross section in the base', 'medulla cross section in the middle', 'medulla cross section in the tip', 'd rambut', 'd medula', 'index medula']]
        set_def = False

        submit_btn = st.button('Train Model')
        if submit_btn:
            st.session_state.submitted = True
            
        if 'submitted' in st.session_state:
            with st.status("Training models...", expanded=True) as status:
                st.write("Pre-processing...")
                time.sleep(2)
                st.write("Fitting the model...")
                time.sleep(1)
                st.write("Evaluating the model...")
                time.sleep(1)
                status.update(label="Finished.", expanded=False)
            
            tree_model, tree_acc, knn_model, knn_acc = model_creation(df)
            save_model(tree_model, 'tree_web')
            save_model(knn_model, 'knn_web')

            with st.container(border=True):
                st.write("Decision Tree C5.0 result:")
                st.metric(label="Accuracy Score", value=tree_acc)
                download_model('db/tree_web.pkl', "Download C5 Model")

            with st.container(border=True):
                st.write("KNN result:")
                st.metric(label="Accuracy Score", value=knn_acc)
                download_model('db/knn_web.pkl', "Download KNN Model")
            # Confirm before replace the current model
            with st.popover("Set as default model"):
                st.write("Do you want to replace the current model with the updated model?")
                set_def = st.button("Confirm")
        if set_def:
            save_model(tree_model, 'def_tree_model')
            save_model(knn_model, 'def_knn_model')
            df.to_excel('db/uploaded_file.xlsx', index=False)

            for key in st.session_state.keys():
                st.session_state.pop(key)
            st.session_state.success = True
            st.rerun()

    except KeyError:
        st.warning("The uploaded file doesn't have the following column: 'spesies', 'color', 'hair cross section in the base', 'hair cross section in the middle', 'hair cross section in the tip', 'medulla cross section in the base', 'medulla cross section in the middle', 'medulla cross section in the tip', 'd rambut', 'd medula', 'index medula'.")
    except ValueError:
        st.warning("Sorry, we only accept files in .xlsx format.")
