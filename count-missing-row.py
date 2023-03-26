import pandas as pd
def count_rows_have_missing_values(data):
    result = 0
    n = data.shape[0]
    for i in range(n):
        is_null = pd.isna(data.loc[i])
        for column in data.columns:
            if is_null[column]:
                result += 1
                break
    print("Số dòng bị thiếu là: ",result)
    return