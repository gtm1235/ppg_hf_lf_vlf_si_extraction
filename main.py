"""
The HRV Analysis library is a Python package for analyzing heart rate variability (HRV) data. The library provides a wide range of tools for calculating HRV statistics, plotting HRV data, and performing time-domain, frequency-domain, and non-linear HRV analyses.

The HRV Analysis library is developed and maintained by the HRV Analysis development team [1]. If you use this library in your research, please cite the following paper:

[1] HRV Analysis Development Team. (2021). hrv-analysis: A Python library for heart rate variability analysis. Zenodo. https://doi.org/10.5281/zenodo.5521308
"""

# ... rest of the code ...

import math
import warnings

import numpy as np
import pandas as pd
from astropy.utils.exceptions import AstropyDeprecationWarning
from hrvanalysis import (get_frequency_domain_features,
                         get_poincare_plot_features)

from find_peaks.peaks_extraction_scaling import find_peaks_and_scale
from hrv_algorithms.hrv_algorithms import (calculate_si,
                                           calculate_derivative_si_time,
                                           process_rr_nn_intervals)
from os_functions.get_csv_directories_and_files import (get_csv_files,
                                                        create_and_check_metric_files)
from utils.utils import (convert_posix_time_to_date,
                         create_time_intervals,
                         create_hrv_window,
                         extract_name_date,
                         hrv_IBI_s_to_ms
                         )


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

# si_values = []
# timestamps = []
# lf_hf = []
# date_timestamps = []

# initialize pd.DataFrames for metrics
metrics_5min_df = None
metrics_15min_df = None
metrics_daily_df = None

# Get a list of all CSV files in the current directory, extract the name and date from each file name, and create and check
# metric files for 5-minute, 15-minute, and daily metrics.
csv_files = get_csv_files()
name, first_date, last_date, files_sorted = extract_name_date(csv_files)
filename_5min_window, filename_15min_window, filename_daily = create_and_check_metric_files(
    name, first_date, last_date)

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
        timestamps = []
        lf_hf = []
        date_timestamps = []

        data = pd.read_csv(file)

        df_hrv = find_peaks_and_scale(data)

        hrv_range = create_time_intervals(minutes_window, df_hrv)
        print(minutes_window, (hrv_range[0]-hrv_range[1])/60000)

        for n in range(len(hrv_range)-1):

            ibi_window_df = create_hrv_window(df_hrv, hrv_range, n)
            ibi_ms = hrv_IBI_s_to_ms(ibi_window_df)

            si_df_interpolated_nn_intervals = process_rr_nn_intervals(ibi_ms)

            if si_df_interpolated_nn_intervals == 0:
                continue

            si = calculate_si(si_df_interpolated_nn_intervals)
            try:
                freq_measures = get_frequency_domain_features(
                    si_df_interpolated_nn_intervals, method='lomb')
            except:
                lf_hf.append(0)

            si_values.append(si)
            timestamps.append(hrv_range[n+1])
            lf_hf.append(freq_measures['lf_hf_ratio'])
            date_timestamps.append(convert_posix_time_to_date(hrv_range[n+1]))


        si_derivative = calculate_derivative_si_time(si_values, timestamps)

        if minutes_window == 5:
            if metrics_5min_df is None:
                si_derivative = np.insert(si_derivative, 0, 0)
            else:
                temp_si_df = ((si_values[0] - metrics_5min_df['si_diff_per_min'].iloc[-1])*60*1000)/(
                    timestamps[0]-metrics_5min_df['timestamp'].iloc[-1])
                si_derivative = np.insert(si_derivative, 0, temp_si_df)

        elif minutes_window == 15:
            if metrics_15min_df is None:
                si_derivative = np.insert(si_derivative, 0, 0)
            else:
                temp_si_df = ((si_values[0] - metrics_15min_df['si_diff_per_min'].iloc[-1])*60*1000)/(
                    timestamps[0]-metrics_15min_df['timestamp'].iloc[-1])
                si_derivative = np.insert(si_derivative, 0, temp_si_df)

        metrics_dict = {'si_values': si_values, 'lf_hf': lf_hf,
                        'si_diff_per_min': si_derivative, 'timestamp': timestamps, 'datetime': date_timestamps}

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
        metrics_daily_df = pd.DataFrame.from_dict(daily_metrics_dict)
    else:
        metrics_daily_df = pd.concat(
            [metrics_daily_df, pd.DataFrame.from_dict(daily_metrics_dict)])


metrics_daily_df.to_csv(filename_daily, index=False)
metrics_5min_df.to_csv(filename_5min_window, index=False)
metrics_15min_df.to_csv(filename_15min_window, index=False)
