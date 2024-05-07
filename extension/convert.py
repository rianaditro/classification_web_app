import pandas as pd

from extension.preprocess_data import mean_df, std_df, percentile

# data standarization
def std_scaled(num, column_index):
    # standarize z = (x - mean) / std
    z = (num - mean_list[column_index]) / std_list[column_index]
    return z

# convert numerical to categorical for C5.0
def to_categoric(num, column_index)->str:
    scaled = std_scaled(num, column_index)
    if scaled <= p_25[column_index]:
        cat = 'under 25%'
    elif scaled <= p_50[column_index]:
        cat = 'under 50%'
    elif scaled <= p_75[column_index]:
        cat = 'under 75%'
    else:
        cat = '75% above'
    return cat


if __name__ == "__main__":
    df = pd.read_excel('db/uploaded_file.xlsx')
# the order are: d rambut, d medula, index medula
    mean_list = mean_df(df)
    std_list = std_df(df)
    p_25, p_50, p_75 = percentile(df)

    n = 0.796722
    print(to_categoric(n, 2))