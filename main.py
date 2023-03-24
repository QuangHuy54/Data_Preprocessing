import pandas as pd
import numpy as np
import argparse

def list_columns_have_missing_values(data):
    result_columns=[]
    for column in data.columns:
        column_content=data[column]
        is_null=pd.isna(column_content)
        for null_check in is_null:
            if null_check:
                result_columns.append(column)
                break
    print(result_columns)
    return
def count_rows_have_missing_values(data):
    result=0
    n=data.shape[0]
    for i in range(n):
        is_null=pd.isna(data.iloc[i])
        for column in data.columns:
            if is_null[column]:
                result+=1
                break
    print(result)
    return
# def calculate_central_tendency(data,mode,column):
#     n=len(data)
#     error_message=""
#     if mode=="mean":
#         result=0
#         count=0
#         for i in range(n):
#             value = data.at[i, column]
#             if not pd.isna(value) and :
#                 count+=1
#                 result+=value
#         if count==0:

# def fill_missing_value(data,mode,columns):
#     n=data.shape[0]
#     for column in columns:
#         if column in data.columns:
#             empty=True
#             for i in range(n):
#                 value=data.at[i,column]
#                 if not pd.isna(value):
#                     empty=False
def remove_row_below_threshold(data,threshold,output_path):
    new_data=pd.DataFrame()
    n=data.shape[0]
    m=data.shape[1]
    for i in range(n):
        count=0
        is_null=pd.isnull(data.iloc[i])
        for column in data.columns:
            if is_null[column]:
                count+=1
        if count*100<=threshold*m:
            new_data=pd.concat([new_data,data.iloc[i].to_frame().T])
    print(new_data)
    return


def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input", help="path of file", required=True)
    args = vars(argParser.parse_args())
    data = pd.read_csv(args['input'])
    print(data.shape)
    list_columns_have_missing_values(data)
    count_rows_have_missing_values(data)
    remove_row_below_threshold(data,10,"hello")
main()