# data standarization
def std_scaled(num, summary:list):
    mean = summary[0]
    std = summary[1]
    # standarize z = (x - mean) / std
    z = (num - mean) / std
    return z

# convert numerical to categorical for C5.0
def to_categoric(num, summary:list)->str:
    mean = summary[0]
    std = summary[1]
    percentile_25 = summary[2]
    percentile_50 = summary[3]
    percentile_75 = summary[4]

    scaled = std_scaled(num, summary)
    if scaled <= percentile_25:
        cat = 'under 25%'
    elif scaled <= percentile_50:
        cat = 'under 50%'
    elif scaled <= percentile_75:
        cat = 'under 75%'
    else:
        cat = '75% above'
    return cat
