import argparse
import pandas as pd


def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "%r not a floating-point literal" % (x,))

    if x <= 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range (0.0, 1.0]" % (x,))
    return x


def remove_col_below_threshold(data: pd.DataFrame, threshold: float, output_path: str) -> pd.DataFrame:
    """
    Remove columns from a pandas DataFrame with missing values exceeding a given threshold.

    Args:
        data (pd.DataFrame): The input DataFrame contain file's data.
        threshold (float): The maximum proportion of missing values allowed in a column.
        output_path (str): The path to the output CSV file.

    Returns:
        pd.DataFrame: The DataFrame with the selected columns removed.

    """

    new_data = []
    num_rows, num_cols = data.shape

    for i in range(num_cols):
        count = data.iloc[:, i].isnull().sum()
        if count / num_rows < threshold:
            new_data.append(data.iloc[:, i])

    new_df = pd.concat(new_data, axis=1)
    new_df.to_csv(output_path, index=False)

    return new_df


if __name__ == '__main__':
    # Parsing the command line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--input", help="path of input file",
                            required=True)  # Adding input's path argument
    arg_parser.add_argument("-t", "--threshold",
                            help="maximum proportion of missing values allowed in a column",
                            type=restricted_float, default=0.1)  # Adding threshold argument
    arg_parser.add_argument("-o", "--output", help="path of output file",
                            default=None)  # Adding output's path argument
    args = vars(arg_parser.parse_args())

    # Reading the csv file and storing it in a data-frame.
    data = pd.read_csv(args['input'])

    # If the user doesn't enter an output file, the program will create an output file
    # with the same name as the input file, but with "_filled" appended to the end.
    if args['output']:
        remove_col_below_threshold(data, args['threshold'], args['output'])
    else:
        remove_col_below_threshold(
            data, args['threshold'], args['input'][:-4] + "_filled.csv")
