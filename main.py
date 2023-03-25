import pandas as pd
import numpy as np
import argparse
from pandas.api.types import is_numeric_dtype

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
        is_null=pd.isna(data.loc[i])
        for column in data.columns:
            if is_null[column]:
                result+=1
                break
    print(result)
    return
def calculate_central_tendency(data,is_missing_data,mode,column):
    n=data.shape[0]
    if not is_numeric_dtype(data[column]):
        frequency=dict()
        max_frequency,filling_value=0,''
        for i in range(n):
            value=data.loc[i,column]
            missing=is_missing_data.loc[i,column]
            if missing:
                continue
            frequency[value]=frequency.get(value,0)+1
            if frequency[value]>max_frequency:
                max_frequency=frequency[value]
                filling_value=value
        return filling_value
    else:
        values=[]
        for i in range(n):
            value=data.loc[i,column]
            missing=is_missing_data.loc[i,column]
            if missing:
                continue
            values.append(value)
        num_nonmissing_values=len(values)
        filling_value=0
        if mode=='mean':
            for i in range(num_nonmissing_values):
                filling_value+=values[i]
            filling_value=filling_value/num_nonmissing_values
        else:
            values.sort()
            index = int(num_nonmissing_values / 2)
            if num_nonmissing_values%2==0:
                filling_value=(values[index]+values[index-1])/2
            else:
                filling_value=values[index]
        return filling_value
def check_empty_column(is_missing_data,column):
    n=is_missing_data.shape[0]
    for i in range(n):
        is_missing=is_missing_data.loc[i,column]
        if not is_missing:
            return False
    return True
def fill_missing_value(data,mode,columns,output_path):
    n=data.shape[0]
    is_missing_data=pd.isna(data)
    for column in columns:
        if column in data.columns:
            if not check_empty_column(is_missing_data,column):
                filling_value=calculate_central_tendency(data,is_missing_data,mode,column)
                for i in range(n):
                    is_missing=is_missing_data.loc[i,column]
                    if is_missing:
                        data.loc[i,column]=filling_value
    data.to_csv(output_path,encoding='utf-8',index=False)
    return

def remove_row_below_threshold(data,threshold,output_path):
    new_data=pd.DataFrame()
    n=data.shape[0]
    m=data.shape[1]
    for i in range(n):
        count=0
        is_null=pd.isnull(data.loc[i])
        for column in data.columns:
            if is_null[column]:
                count+=1
        if count*100<=threshold*m:
            new_data=pd.concat([new_data,data.loc[i].to_frame().T])
    print(new_data)
    return


def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input", help="path of file", required=True)
    args = vars(argParser.parse_args())
    data = pd.read_csv(args['input'])
    # data['LotFrontage'].fillna(data['LotFrontage'].median(),inplace=True)
    # data['Fence'].fillna(data['Fence'].mode()[0],inplace=True)
    # data.to_csv("output1.csv", encoding='utf-8', index=False)
    list_columns_have_missing_values(data)
    count_rows_have_missing_values(data)
    fill_missing_value(data,"median",['LotFrontage','Fence'],"output.csv")

main()