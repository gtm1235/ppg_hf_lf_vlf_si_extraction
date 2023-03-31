import os
from typing import List


def get_csv_files() -> List[str]:
    """
    Get a list of CSV files in directories containing 'csv' in their names.

    Returns:
        A list of file paths for CSV files in directories containing 'csv' in their names.
    """

    current_dir = os.getcwd()

    csv_files = []

    for item in os.listdir(current_dir):
        if os.path.isdir(item) and "csv" in item.lower():
            for filename in os.listdir(item):
                if filename.endswith(".csv"):
                    csv_files.append(os.path.join(item, filename))

    return csv_files

def check_file_exists(filename: str) -> None:
    """
    Checks if a file with the given filename exists. If the file exists, it is deleted and a new file is created. If
    the file does not exist, a new file is created.

    Args:
        filename (str): The name of the file to check/create.

    Returns:
        None: The function does not return anything.
    """

    # Check if the file exists.
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File '{filename}' deleted.")
    
    # Create the file.
    with open(filename, 'w') as file:
        print(f"File '{filename}' created.")


def create_and_check_metric_files(name: str, first_date: str, last_date: str) -> None:
    """
    Creates and checks the existence of metric files for a range of dates.

    Args:
        name (str): The name of the metric file.
        first_date (str): The starting date of the range in 'YYYY-MM-DD' format.
        last_date (str): The ending date of the range in 'YYYY-MM-DD' format.

    Returns:
        None: The function does not return anything. It raises an exception if any of the files do not exist.
    """
    
    # Create filenames for different metric files.
    filename_daily = f'{name}_{first_date}_to_{last_date}_daily.csv'
    filename_5min_window = f'{name}_{first_date}_to_{last_date}_5min.csv'
    filename_15min_window = f'{name}_{first_date}_to_{last_date}_15min.csv'
    
    # Check if metric files exist.
    check_file_exists(filename_daily)
    check_file_exists(filename_5min_window)
    check_file_exists(filename_15min_window)

    return filename_5min_window, filename_15min_window, filename_daily
