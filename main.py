import pandas as pd
import numpy as np
import argparse
from pandas.api.types import is_numeric_dtype




def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input", help="path of file", required=True)
    args = vars(argParser.parse_args())
    data = pd.read_csv(args['input'])
    # data['LotFrontage'].fillna(data['LotFrontage'].median(),inplace=True)
    # data['Fence'].fillna(data['Fence'].mode()[0],inplace=True)
    # data.to_csv("output1.csv", encoding='utf-8', index=False)


main()
