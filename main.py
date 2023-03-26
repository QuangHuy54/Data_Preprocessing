import pandas as pd
import numpy as np
import argparse
from count_missing_row import count_rows_have_missing_values
from impute import fill_missing_value
from list_missing_col import list_columns_have_missing_values
from remove_missing_row_below_threshold import remove_row_missing_with_threshold
from remove_missing_col_below_threshold import remove_col_below_threshold
from normalization import normalize_attribute

def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input", help="path of input file", required=True)
    argParser.add_argument("-o", "--output", help="path of output file")
    subParser=argParser.add_subparsers(dest='choice')
    list_missing_col_parser=subParser.add_parser('listmc',help="List columns have missing values.")
    count_missing_row_parser=subParser.add_parser('countmr',help="Count rows have missing values.")
    fill_missing_value_parser=subParser.add_parser('fillnull',help='Fill missing values')
    fill_missing_value_parser.add_argument('-m','--method',choices=['mean','median'],required=True)
    fill_missing_value_parser.add_argument('-c','--column',nargs='+',required=True)
    remove_missing_parser=subParser.add_parser('removena',help="Remove rows or columns missing values with threshold")
    remove_missing_parser.add_argument('-a','--axis',type=int,choices=[0,1],required=True)
    remove_missing_parser.add_argument('-t','--threshold',type=float,required=True)
    remove_duplicate_parser=subParser.add_parser('removedup',help="Remove duplicate rows")
    normalize_parser=subParser.add_parser('normalize',help="Normalize attributes")
    normalize_parser.add_argument('-m','--method',choices=['minmax','zscore'],required=True)
    normalize_parser.add_argument('-c','--column',nargs='+',required=True)
    calculate_parser=subParser.add_parser('calculate',help='Calculate an expression')
    calculate_parser.add_argument('-e','--expression',required=True)
    calculate_parser.add_argument('-c','--column',nargs='+',required=True)
    calculate_parser.add_argument('-n','--name',required=True,help='Name of the new column.')
    args = argParser.parse_args()
    data = pd.read_csv(args.input)
    # data['LotFrontage'].fillna(data['LotFrontage'].median(),inplace=True)
    # data['Fence'].fillna(data['Fence'].mode()[0],inplace=True)
    # data.to_csv("output1.csv", encoding='utf-8', index=False
    temp_data=data.copy()
    test_data=temp_data['LotFrontage']
    temp_data['LotFrontage']=(test_data-test_data.min())/(test_data.max()-test_data.min())
    temp_data.to_csv("output1.csv", encoding='utf-8', index=False)
    try:
        if args.choice=='listmc':
            list_columns_have_missing_values(data)
        elif args.choice=='countmr':
            count_rows_have_missing_values(data)
        elif args.choice=='fillnull':
            fill_missing_value(data,args.method,args.column,args.output)
        elif args.choice=='removena':
            if args.axis==0:
                remove_row_missing_with_threshold(data,args.threshold,args.output)
            else:
                remove_col_below_threshold(data,args.threshold,args.output)
        elif args.choice=='normalize':
            normalize_attribute(data,args.method,args.column,args.output)
    except Exception as e:
        print(e)
main()
