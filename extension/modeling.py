from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier  
from sklearn.metrics import accuracy_score
from C45 import C45Classifier

from extension.preprocess_data import pre_processing

# this is the processing for modelling
def data_training(dataset, model):
    y = dataset['spesies']
    X = dataset.drop(['spesies'], axis=1)

    # split data into train:test 80:20
    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2, stratify=y)
    # model training
    model.fit(train_x, train_y)
    # evaluate model
    prediction = model.predict(test_x)
    accuracy = accuracy_score(test_y, prediction)
    accuracy = "{:.2%}".format(accuracy)
    return model, accuracy

# this is the big function of modelling
def model_creation(df):
    df, tree_df, knn_df = pre_processing(df)
    tree = C45Classifier()
    knn = KNeighborsClassifier()
    tree_model, tree_acc = data_training(tree_df, tree)
    knn_model, knn_acc = data_training(knn_df, knn)
    return tree_model, tree_acc, knn_model, knn_acc
