import pandas as pd


df = pd.read_excel('db/summary_df.xlsx')
# the order are: d rambut, d medula, index medula
mean = df['mean'].to_list()
std = df['std'].to_list()
p_25 = df['25%'].to_list()
p_50 = df['50%'].to_list()
p_75 = df['75%'].to_list()


# convert numerical to categorical for C5.0
def to_categoric(num, col_idx)->str:
    # z = (x-mean)/std
    scaled = (num - mean[col_idx])/std[col_idx]
    if scaled <= p_25[col_idx]:
        cat = 'under 25%'
    elif scaled <= p_50[col_idx]:
        cat = 'under 50%'
    elif scaled <= p_75[col_idx]:
        cat = 'under 75%'
    else:
        cat = '75% above'

    return cat


if __name__ == "__main__":
    n = 0.796722
    print(to_categoric(n, 2))