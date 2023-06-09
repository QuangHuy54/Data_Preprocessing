import pandas as pd
import argparse


def remove_duplicate_samples(data: pd.DataFrame, output_path: str) -> pd.DataFrame:
    """
    We loop through the rows of the dataframe, convert each row to a tuple, and add it to a set. If we
    have not seen the row before, we add it to a list of indices to keep. We then use this list of
    indices to keep to create a new dataframe with only the unique rows

    :param data: The dataframe that we want to remove duplicate rows from
    :type data: pd.DataFrame
    :param output_path: The path to the CSV file that you want to write the unique data to
    :type output_path: str
    :return: The unique dataframe
    """

    # Initialize an empty list to store the indices of the rows to keep
    indices_to_keep = []

    # Create a set to keep track of the rows that we have seen
    seen_rows = set()

    # Loop through the rows of the dataframe
    for index in range(0, data.shape[0]):
        # Convert the row to a tuple so it can be added to a set
        row_tuple = tuple(["" if pd.isna(e) else e for e in data.iloc[index]])

        # If we have not seen this row before, add it to the list of indices to keep and the set of seen rows
        if row_tuple not in seen_rows:
            seen_rows.add(row_tuple)
            indices_to_keep.append(index)

    # Use the list of indices to keep to create a new dataframe with only the unique rows
    unique_data = data.iloc[indices_to_keep]

    # Write the unique data to a CSV file
    unique_data.to_csv(output_path, index=False)
    print("Saved to", output_path)
    return unique_data


if __name__ == '__main__':
    # Parsing the command line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input", help="path of file",
                           required=True)  # Adding input's path argument
    argParser.add_argument("-o", "--output", help="path of output file",
                           required=False)  # Adding output's path argument
    args = vars(argParser.parse_args())

    # Reading the csv file and storing it in a data-frame.
    data = pd.read_csv(args['input'])

    # Removing duplicate rows from the data-frame and writing the unique data to a new file.
    remove_duplicate_samples(data, args['output'] or (
        args['input'][:-4] + "_unique.csv"))
