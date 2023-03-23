import pandas as pd
import argparse

def list_columns_have_missing_values(data):
    result_columns=[]
    for column in data.columns:
        column_content=data[column]
        for content in column_content:
            if pd.isna(content):
                result_columns.append(column)
                break
    print(result_columns)
    return
def count_rows_have_missing_values(data):
    result=0
    for i in range(len(data)):
        for column in data.columns:
            value=data.at[i,column]
            if pd.isna(value):
                result+=1
                break
    print(result)
    return

def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input", help="path of file", required=True)
    args = vars(argParser.parse_args())
    data = pd.read_csv(args['input'])
    list_columns_have_missing_values(data)
    count_rows_have_missing_values(data)

main()
