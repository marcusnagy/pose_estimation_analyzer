import os
import sys
import pandas as pd


def is_csv_file(filename):
    return filename.endswith('.csv')


def read_csv_file(filepath):
    return pd.read_csv(filepath, index_col=0)


def check_file_format(df_list):
    ref_columns = df_list[0].columns
    for df in df_list:
        if not df.columns.equals(ref_columns):
            raise ValueError("Files do not have the same format")
    return True


def min_max_values(df_list):
    result = {}
    for column in df_list[0].columns:
        max_val = max(df[column].max() for df in df_list)
        min_val = min(df[column].min() for df in df_list)
        result[column] = (min_val, max_val)
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python min_max.py <file1.csv> <file2.csv> ...")
        return

    csv_filepaths = sys.argv[1:]

    for filepath in csv_filepaths:
        if not is_csv_file(filepath):
            print(f"Error: {filepath} is not a CSV file")
            return

    df_list = [read_csv_file(f) for f in csv_filepaths]

    if not check_file_format(df_list):
        print("Error: Not all CSV files have the same format")
        return

    result = min_max_values(df_list)

    for column, (min_val, max_val) in result.items():
        print(f"Column: {column} - Min: {min_val}, Max: {max_val}")


if __name__ == "__main__":
    main()
