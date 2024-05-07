import streamlit as st
import pandas as pd
import pickle

from C45 import C45Classifier
from sklearn.neighbors import KNeighborsClassifier
from collections import Counter


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
    with st.form("user_input"):
        st.write("Input Data")
        color_input = st.selectbox("color", options=color_value)
        hair_base_input = st.selectbox("hair cross section in the base", options=hair_base_value)
        hair_middle_input = st.selectbox("hair cross section in the middle", options=hair_middle_value)
        hair_tip_input = st.selectbox("hair cross section in the tip", options=hair_tip_value)
        medula_base_input = st.selectbox("medulla cross section in the base", options=medula_base_value)
        medula_middle_input = st.selectbox("medulla cross section in the middle", options=medula_middle_value)
        medula_tip_input = st.selectbox("medulla cross section in the tip", options=medula_tip_value)
        d_rambut_input = st.number_input("d rambut",step=0)
        d_medula_input = st.number_input("d medula",step=0)
        index_medula_input = st.number_input("index medula",step=1e-7,format="%.6f")

        tree_input = [{'color': color_input,
                    'hair cross section in the base': hair_base_input,
                    'hair cross section in the middle': hair_middle_input,
                    'hair cross section in the tip': hair_tip_input,
                    'medulla cross section in the base': medula_base_input,
                    'medulla cross section in the middle': medula_middle_input,
                    'medulla cross section in the tip': medula_tip_input,
                    'd rambut cat': to_categoric(d_rambut_input, rambut_summary),
                    'd medula cat': to_categoric(d_medula_input, medula_summary),
                    'index medula cat': to_categoric(index_medula_input, index_summary)}]
        
        knn_input = [[color_value.index(color_input), 
                      hair_base_value.index(hair_base_input), 
                      hair_middle_value.index(hair_middle_input), 
                      hair_tip_value.index(hair_tip_input), 
                      medula_base_value.index(medula_base_input), 
                      medula_middle_value.index(medula_middle_input), 
                      medula_tip_value.index(medula_tip_input), 
                      std_scaled(d_rambut_input, rambut_summary), 
                      std_scaled(d_medula_input, medula_summary), 
                      std_scaled(index_medula_input, index_summary)]]
        
        submit_btn = st.form_submit_button("Submit")

        if submit_btn:
            predicted = [tree_model.predict(tree_input)[0], knn_predict(knn_input)]

    if predicted is not None:
         st.write(f"Hasil prediksi: {predicted[0]}")
         st.write("Tingkat kemiripan dengan kelas lain:")
         for key, value in predicted[1].items():
              st.write(f"{key}: {value}%")


if __name__ == "__main__":
    main()