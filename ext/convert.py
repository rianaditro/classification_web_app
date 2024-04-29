import pandas as pd


df = pd.read_excel('db/summary_df.xlsx')
# the order are: d rambut, d medula, index medula
mean = df['mean'].to_list()
std = df['std'].to_list()
p_25 = df['25%'].to_list()
p_50 = df['50%'].to_list()
p_75 = df['75%'].to_list()


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

def std_scaled(num, column_index):
    # standarize z = (x - mean) / std
    z = (num - mean[column_index]) / std[column_index]
    return z


if __name__ == "__main__":
    n = 0.796722
    print(to_categoric(n, 2))