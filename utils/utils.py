import pandas as pd
import numpy as np
import os
#from main import NUM_MINUTES_WINDOW

def create_time_intervals(num, data):
    """Create a list of time wondows based on window size. Uses max and min timestamps from each nights sleep"""
    num_min = num
    max_ts = data['ts'].iloc[-1]
    min_ts = data['ts'].iloc[0]
    sleep_min = (max_ts-min_ts)/60000
    number = int(sleep_min/num_min)
    hrv_range = np.linspace(data['ts'].iloc[0], data['ts'].iloc[-1], num=number)
    hrv_range = hrv_range.astype(np.int64)

    return hrv_range
    
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

# Check if file exists
def check_file_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File '{filename}' deleted.")
        with open(filename, 'w') as file:
            print(f"File '{filename}' created.")
    else:
        with open(filename, 'w') as file:
            print(f"File '{filename}' created.")

def convert_posix_time_to_date(posix_time):
    """Converts posix time to date"""
    # date = pd.to_datetime(posix_time, unit='ms')
    # date = date.strftime('%Y-%m-%d %H:%M:%S')
    # return date
    return pd.to_datetime(posix_time, unit='ms').strftime('%Y-%m-%d %H:%M:%S')