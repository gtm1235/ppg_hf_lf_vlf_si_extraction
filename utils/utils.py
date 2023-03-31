import pandas as pd
import numpy as np

from typing import List
#from main import NUM_MINUTES_WINDOW

def create_time_intervals(number_of_minutes: int, data: pd.DataFrame) -> np.ndarray:
    """
    Create a list of time windows based on window size.
    
    Uses max and min timestamps from each night's sleep to calculate the number of
    time windows based on the provided number of minutes. Returns a numpy array of 
    time windows as integers.
    
    Args:
        number_of_minutes (int): Size of each time window in minutes.
        data (pd.DataFrame): DataFrame containing HRV data with a 'ts' column of timestamps.
        
    Returns:
        np.ndarray: Array of integers representing time windows.
    """
    max_ts = data['ts'].iloc[-1]
    min_ts = data['ts'].iloc[0]
    sleep_min = (max_ts-min_ts)/60000
    number = int(sleep_min/number_of_minutes)
    return np.linspace(data['ts'].iloc[0], data['ts'].iloc[-1], num=number).astype(np.int64)


def create_hrv_window(df_hrv: pd.DataFrame, hrv_range: np.ndarray[np.int64], n: int) -> pd.DataFrame:
    """
    Creates a time range window of Interbeat Intervals (IBI) for short term recovery calculations.

    Args:
    - df_hrv (pd.DataFrame): A pandas DataFrame containing HRV data.
    - hrv_range (List[int]): A list of integers representing time range windows for HRV analysis.
    - n (int): An integer representing the index of the current time range window in hrv_range.

    Returns:
    - si_df (pd.DataFrame): A pandas DataFrame containing HRV data within the current time range window.
    """
    si_df = df_hrv.loc[df_hrv['ts'] < hrv_range[n+1]]
    si_df = si_df.loc[si_df['ts'] > hrv_range[n]]
    return si_df

def hrv_IBI_s_to_ms(si_df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the 'hrv' column IBIs of a DataFrame from seconds to milliseconds.

    Args:
    - si_df (pd.DataFrame): A pandas DataFrame containing HRV data in a window.

    Returns:
    - si_np (np.ndarray): A pandas DataFrame containing HRV data IBIs in  milliseconds.
    """
    si_np = (si_df['hrv'].to_numpy())*1000
    return si_np

def median_bin_count(edges, median):
    count = 0
    for edge in edges:
        if median > edge:
            count += 1
        else:
            break
            
    return count

def extract_name_date(files):
    split_files = [file.split('.') for file in files]
    files_sorted = sorted(split_files, key=lambda x: x[2])
    #print(files_sorted)
    name = files_sorted[0][0].split('\\')[1]
    first_date = files_sorted[0][2]
    last_date = files_sorted[-1][2]
    #print(files_sorted)
    return name, first_date, last_date, files_sorted



def convert_posix_time_to_date(posix_time):
    """Converts posix time to date"""
    # date = pd.to_datetime(posix_time, unit='ms')
    # date = date.strftime('%Y-%m-%d %H:%M:%S')
    # return date
    return pd.to_datetime(posix_time, unit='ms').strftime('%Y-%m-%d %H:%M:%S')


# def create_and_check_metric_files()
#     # file for range of dates for daily metrics
#     filename_daily = f'{name}_{first_date}_to_{last_date}_daily.csv'
#     check_file_exists(filename_daily)
#     # file for range of dates for 5 min metrics
#     filename_5min_window = f'{name}_{first_date}_to_{last_date}_5min.csv'
#     check_file_exists(filename_5min_window)
#     # file for range of dates for 15 min metrics
#     filename_15min_window = f'{name}_{first_date}_to_{last_date}_15min.csv'
#     check_file_exists(filename_15min_window)


# def check_file_exists(filename: str) -> None:
#     """
#     Checks if a file with the given filename exists. If the file exists, it is deleted and a new file is created. If
#     the file does not exist, a new file is created.

#     Args:
#         filename (str): The name of the file to check/create.

#     Returns:
#         None: The function does not return anything.
#     """

#     # Check if the file exists.
#     if os.path.exists(filename):
#         os.remove(filename)
#         print(f"File '{filename}' deleted.")
    
#     # Create the file.
#     with open(filename, 'w') as file:
#         print(f"File '{filename}' created.")


# def create_and_check_metric_files(name: str, first_date: str, last_date: str) -> None:
#     """
#     Creates and checks the existence of metric files for a range of dates.

#     Args:
#         name (str): The name of the metric file.
#         first_date (str): The starting date of the range in 'YYYY-MM-DD' format.
#         last_date (str): The ending date of the range in 'YYYY-MM-DD' format.

#     Returns:
#         None: The function does not return anything. It raises an exception if any of the files do not exist.
#     """
    
#     # Create filenames for different metric files.
#     filename_daily = f'{name}_{first_date}_to_{last_date}_daily.csv'
#     filename_5min_window = f'{name}_{first_date}_to_{last_date}_5min.csv'
#     filename_15min_window = f'{name}_{first_date}_to_{last_date}_15min.csv'
    
#     # Check if metric files exist.
#     check_file_exists(filename_daily)
#     check_file_exists(filename_5min_window)
#     check_file_exists(filename_15min_window)





