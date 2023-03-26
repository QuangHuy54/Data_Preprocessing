import pandas as pd
from pandas.api.types import is_numeric_dtype

def calculate_central_tendency(data, is_missing_data, mode, column):
    n = data.shape[0]
    if not is_numeric_dtype(data[column]):
        frequency = dict()
        max_frequency, filling_value = 0, ''
        for i in range(n):
            value = data.loc[i, column]
            missing = is_missing_data.loc[i, column]
            if missing:
                continue
            frequency[value] = frequency.get(value, 0)+1
            if frequency[value] > max_frequency:
                max_frequency = frequency[value]
                filling_value = value
        return filling_value
    else:
        values = []
        for i in range(n):
            value = data.loc[i, column]
            missing = is_missing_data.loc[i, column]
            if missing:
                continue
            values.append(value)
        num_nonmissing_values = len(values)
        filling_value = 0
        if mode == 'mean':
            for i in range(num_nonmissing_values):
                filling_value += values[i]
            filling_value = filling_value/num_nonmissing_values
        else:
            values.sort()
            index = int(num_nonmissing_values / 2)
            if num_nonmissing_values % 2 == 0:
                filling_value = (values[index]+values[index-1])/2
            else:
                filling_value = values[index]
        return filling_value


def check_empty_column(is_missing_data, column):
    n = is_missing_data.shape[0]
    for i in range(n):
        is_missing = is_missing_data.loc[i, column]
        if not is_missing:
            return False
    return True


def fill_missing_value(data, mode, columns, output_path):
    n = data.shape[0]
    is_missing_data = pd.isna(data)
    for column in columns:
        if column in data.columns:
            if not check_empty_column(is_missing_data, column):
                filling_value = calculate_central_tendency(
                    data, is_missing_data, mode, column)
                for i in range(n):
                    is_missing = is_missing_data.loc[i, column]
                    if is_missing:
                        data.loc[i, column] = filling_value
    data.to_csv(output_path, encoding='utf-8', index=False)
    return