import pandas as pd
import math
from pandas.api.types import is_numeric_dtype
from impute import calculate_central_tendency, check_empty_column

def calculate_standard_deviation(data, is_missing_data, column):
    mean = calculate_central_tendency(data, is_missing_data, 'mean', column)
    n = data.shape[0]
    sd = 0
    non_missing_num = 0
    for i in range(n):
        value = data.loc[i, column]
        is_missing = is_missing_data.loc[i, column]
        if not is_missing:
            sd += (value - mean) ** 2
            non_missing_num += 1
    sd = math.sqrt(sd / (non_missing_num - 1))
    return sd


def max_min_value(data, is_missing_data, column):
    n = data.shape[0]
    max_value = -math.inf
    min_value = math.inf
    for i in range(n):
        value = data.loc[i, column]
        is_missing = is_missing_data.loc[i, column]
        if not is_missing:
            max_value = max(max_value, value)
            min_value = min(min_value, value)
    return max_value, min_value


def normalize_attribute(data, mode, columns, output_path):
    n = data.shape[0]
    is_missing_data = pd.isna(data)
    for column in columns:
        if column in data.columns:
            if not check_empty_column(is_missing_data, column) and is_numeric_dtype(data[column]):
                if mode == 'minmax':
                    max_value, min_value = max_min_value(data, is_missing_data, column)
                    for i in range(n):
                        is_missing = is_missing_data.loc[i, column]
                        if not is_missing:
                            x = data.loc[i, column]
                            data.loc[i, column] = (x - min_value) / (max_value - min_value)
                elif mode == 'zscore':
                    mean = calculate_central_tendency(data, is_missing_data, 'mean', column)
                    sd = calculate_standard_deviation(data, is_missing_data, column)
                    for i in range(n):
                        is_missing = is_missing_data.loc[i, column]
                        if not is_missing:
                            x = data.loc[i, column]
                            data.loc[i, column] = (x - mean) / sd
    data.to_csv(output_path, encoding='utf-8', index=False)
    return
