# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv
import sys
from pathlib import Path

# Default CSV file path for banking data
csv_dir = "data"
csv_output_dir = csv_dir + "/" + "output"
csv_name = "daily_rate_sheet.csv"
csv_path = csv_dir + "/" + csv_name

def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data

def save_csv(path, data):
    if not Path(csv_output_dir).exists():
        Path(csv_output_dir).mkdir(parents=True, exist_ok=True)

    with open(path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for row in data:
            csvwriter.writerow(row)


def load_bank_data():
    """Loads banking data from CSV file.
    The default path is "data/daily_rate_sheet.csv"

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = Path(csv_path)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)