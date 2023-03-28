import math
import warnings

import numpy as np
import pandas as pd
from astropy.utils.exceptions import AstropyDeprecationWarning
from hrvanalysis import (get_frequency_domain_features,
                         get_poincare_plot_features)

from find_peaks.peaks_extraction_scaling import find_peaks_and_scale
from hrv_algorithms.hrv_algorithms import calculate_si, process_rr_nn_intervals
from os_functions.get_csv_directories_and_files import get_csv_files
from utils.utils import (check_file_exists, convert_posix_time_to_date,
                         create_time_intervals, extract_name_date)

# Set pandas and numpy floatdisplay options to supress scientific notation
pd.options.display.float_format = '{:20,.2f}'.format
np.set_printoptions(suppress=True, formatter={'float_kind': '{:0}'.format})

# Suppress warnings of type DeprecationWarning
warnings.simplefilter("ignore", category=DeprecationWarning)
warnings.simplefilter('ignore', category=AstropyDeprecationWarning)
warnings.simplefilter('ignore', category=FutureWarning)
warnings.simplefilter('ignore', category=RuntimeWarning)

# set number of minutes for sliding window in calculation for SI, HF/LF, VLF, Poincare
NUM_MINUTES_WINDOW = [5, 15]

si_values = []
time_list = []
lf_hf_list = []
date_time_list = []
metrics_5min_df = None
metrics_15min_df = None
metrics_daily_df = None

csv_files = get_csv_files()

# extarct information from filename
name, first_date, last_date, files_sorted = extract_name_date(csv_files)

# file for range of dates for daily metrics
filename_daily = f'{name}_{first_date}_to_{last_date}_daily.csv'
check_file_exists(filename_daily)
# file for range of dates for 5 min metrics
filename_5min_window = f'{name}_{first_date}_to_{last_date}_5min.csv'
check_file_exists(filename_5min_window)
# file for range of dates for 15 min metrics
filename_15min_window = f'{name}_{first_date}_to_{last_date}_15min.csv'
check_file_exists(filename_15min_window)

for file in files_sorted:
    current_date = file[2]
    current_date = current_date[:4] + '-' + \
        current_date[4:6] + '-' + current_date[6:]
    file = '.'.join(file)

    for minutes_window in NUM_MINUTES_WINDOW:
        vlf_list = []
        total_power_list = []
        si_sleep = []
        sd_list = [[], [], []]
        si_values = []
        time_list = []
        lf_hf_list = []
        date_time_list = []

        data = pd.read_csv(file)

        df_hrv = find_peaks_and_scale(data)

        hrv_range = create_time_intervals(minutes_window, df_hrv)
        print(minutes_window, (hrv_range[0]-hrv_range[1])/60000)

        for n in range(len(hrv_range)-1):
            # Caluclates values over window range for short term recovery
            si_df = df_hrv.loc[df_hrv['ts'] < hrv_range[n+1]]
            si_df = si_df.loc[si_df['ts'] > hrv_range[n]]
            si_np = si_df['hrv'].to_numpy()
            si_np = si_np*1000

            si_df_interpolated_nn_intervals = process_rr_nn_intervals(si_np)

            if si_df_interpolated_nn_intervals == 0:
                continue

            si = calculate_si(si_df_interpolated_nn_intervals)
            try:
                freq_measures = get_frequency_domain_features(
                    si_df_interpolated_nn_intervals, method='lomb')
            except:
                lf_hf_list.append(0)

            si_values.append(si)
            time_list.append(hrv_range[n+1])
            lf_hf_list.append(freq_measures['lf_hf_ratio'])
            date_time_list.append(convert_posix_time_to_date(hrv_range[n+1]))

        si_values_np = np.array(si_values)
        si_diff_np = np.diff(si_values_np)
        time_values_np = np.array(time_list)
        time_diff_np = np.diff(time_values_np)
        si_diff = ((si_diff_np*1000*60)/time_diff_np)

        if minutes_window == 5:
            if metrics_5min_df is None:
                si_diff = np.insert(si_diff, 0, 0)
            else:
                temp_si_df = ((si_values[0] - metrics_5min_df['si_diff_per_min'].iloc[-1])*60*1000)/(
                    time_list[0]-metrics_5min_df['timestamp'].iloc[-1])
                si_diff = np.insert(si_diff, 0, temp_si_df)

        elif minutes_window == 15:
            if metrics_15min_df is None:
                si_diff = np.insert(si_diff, 0, 0)
            else:
                temp_si_df = ((si_values[0] - metrics_15min_df['si_diff_per_min'].iloc[-1])*60*1000)/(
                    time_list[0]-metrics_15min_df['timestamp'].iloc[-1])
                si_diff = np.insert(si_diff, 0, temp_si_df)

        metrics_dict = {'si_values': si_values, 'lf_hf_list': lf_hf_list,
                        'si_diff_per_min': si_diff, 'timestamp': time_list, 'datetime': date_time_list}

        if minutes_window == 5:

            if metrics_5min_df is None:
                # If the DataFrame doesn't exist, create it and assign it the dictionary
                metrics_5min_df = pd.DataFrame.from_dict(metrics_dict)
            else:
                metrics_5min_df = pd.concat(
                    [metrics_5min_df, pd.DataFrame.from_dict(metrics_dict)])

        elif minutes_window == 15:
            if metrics_15min_df is None:
                # If the DataFrame doesn't exist, create it and assign it the dictionary
                metrics_15min_df = pd.DataFrame.from_dict(metrics_dict)
            else:
                metrics_15min_df = pd.concat(
                    [metrics_15min_df, pd.DataFrame.from_dict(metrics_dict)])

    # Calculate overnight values to show slow recovery
    si_np = df_hrv['hrv'].to_numpy()
    si_np = si_np*1000
    si_df_interpolated_nn_intervals = process_rr_nn_intervals(si_np)

    if si_df_interpolated_nn_intervals == 0:
        continue

    sd_info = get_poincare_plot_features(si_df_interpolated_nn_intervals)
    if 'sd1' not in sd_info:
        sd_list[0].append(0)
    if 'sd2' not in sd_info:
        sd_list[1].append(0)
    if 'ratio_sd2_sd1' not in sd_info:
        sd_list[2].append(0)

    si = calculate_si(si_df_interpolated_nn_intervals)

    try:
        freq_measures = get_frequency_domain_features(
            si_df_interpolated_nn_intervals, method='lomb')
    except:
        vlf_list.append(0)
        total_power_list.append(0)

    si_sleep.append(si)
    vlf_list.append(math.log(freq_measures['vlf']))
    total_power_list.append(math.log(freq_measures['total_power']))

    sd_list[0].append(sd_info['sd1'])
    sd_list[1].append(sd_info['sd2'])
    sd_list[2].append(sd_info['ratio_sd2_sd1'])

    try:
        vlf_percent = freq_measures['vlf']/freq_measures['total_power']
    except ZeroDivisionError:
        vlf_percent = 0

    daily_metrics_dict = {
        'si_values': si_sleep,
        'vlf_list': vlf_list,
        'total_power': total_power_list,
        'vlf/tp': vlf_percent,
        'sd1': sd_list[0],
        'sd2': sd_list[1],
        'sd_ratio': sd_list[2],
        'date': current_date
    }

    if metrics_daily_df is None:
        # If the DataFrame doesn't exist, create it and assign it the dictionary
        metrics_daily_df = pd.DataFrame.from_dict(metrics_dict)
    else:
        metrics_daily_df = pd.concat(
            [metrics_daily_df, pd.DataFrame.from_dict(metrics_dict)])


metrics_daily_df.to_csv(filename_daily, index=False)
metrics_5min_df.to_csv(filename_5min_window, index=False)
metrics_15min_df.to_csv(filename_15min_window, index=False)
