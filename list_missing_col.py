import pandas as pd
import argparse

def list_columns_have_missing_values(data):
    result_columns = []
    for column in data.columns:
        column_content = data[column]
        is_null = pd.isna(column_content)
        for null_check in is_null:
            if null_check:
                result_columns.append(column)
                break
    print("Có tổng cộng ",len(result_columns)," cột bị thiếu dữ liệu.")
    print("Danh sách các cột có giá trị bị thiếu: ",result_columns)
    return

if __name__ == '__main__':
    # Parsing the command line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input", help="path of file", required=True)
    args = vars(argParser.parse_args())

    # Reading the csv file and storing it in a data-frame.
    data = pd.read_csv(args['input'])

    # Printing the names of the columns in the file's data that have missing values.
    list_columns_have_missing_values(data)
