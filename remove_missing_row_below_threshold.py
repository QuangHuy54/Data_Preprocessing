import pandas as pd
def remove_row_missing_with_threshold(data, threshold, output_path):
    new_data = pd.DataFrame()
    n = data.shape[0]
    m = data.shape[1]
    for i in range(n):
        count = 0
        is_null = pd.isnull(data.loc[i])
        for column in data.columns:
            if is_null[column]:
                count += 1
        if count <= threshold*m:
            new_data = pd.concat([new_data, data.loc[i].to_frame().T])
    new_data.to_csv(output_path, encoding='utf-8', index=False)
    return