import pandas as pd
import argparse


def list_columns_have_missing_values(data: pd.DataFrame) -> None:
    """
    Prints the names of the columns in the file's data that have missing values.

    Parameters:
        data (pd.DataFrame): The DataFrame of file's data to analyze for missing values.
    Returns:
        None
    """

    # Iterates over the columns of the dataframe
    # and takes the column name if the column has any missing values.
    result_cols = [col for col in data.columns if data[col].isnull().any()]
    print(result_cols)
    return


if __name__ == '__main__':
    # Parsing the command line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input", help="path of file", required=True)
    args = vars(argParser.parse_args())

    # Reading the csv file and storing it in a dataframe.
    data = pd.read_csv(args['input'])

    # Printing the names of the columns in the file's data that have missing values.
    list_columns_have_missing_values(data)
