# data standarization for KNN
def std_scaled(num, summary:list):
    mean = summary[0]
    std = summary[1]
    # standarize z = (x - mean) / std
    z = (num - mean) / std
    return z

# convert numerical to categorical for C5.0
def to_categoric(num, summary:list)->str:
    percentile_25 = summary[2]
    percentile_50 = summary[3]
    percentile_75 = summary[4]

    if num <= percentile_25:
        cat = 'under 25%'
    elif num <= percentile_50:
        cat = 'under 50%'
    elif num <= percentile_75:
        cat = 'under 75%'
    else:
        cat = '75% above'
    return cat
