import pandas as pd
import numpy as np

import math 
import matplotlib.pyplot as plt
from statistics import mean
from hrvanalysis import (
    get_frequency_domain_features, 
    plot_psd, plot_poincare, 
    get_poincare_plot_features
)

import warnings
from astropy.utils.exceptions import AstropyDeprecationWarning

from os_functions.get_csv_directories_and_files import get_csv_files
from find_peaks.peaks_extraction_scaling import find_peaks_and_scale
from hrv_algorithms.hrv_algorithms import calculate_si, process_rr_nn_intervals
from utils.utils import create_time_intervals, extract_name_date, check_file_exists

pd.options.display.float_format = '{:20,.2f}'.format
np.set_printoptions(suppress=True, formatter={'float_kind':'{:0}'.format})

# Suppress warnings of type DeprecationWarning
warnings.simplefilter("ignore", category=DeprecationWarning)
warnings.simplefilter('ignore', category=AstropyDeprecationWarning)
warnings.simplefilter('ignore', category=FutureWarning)
warnings.simplefilter('ignore', category=RuntimeWarning)



NUM_MINUTES_WINDOW = 5  #set number of minutes for sliding window in calculation for SI, HF/LF, VLF, Poincare

si_values = []
time_list = []
lf_hf_list = []
vlf_list = []
total_power_list = []
si_sleep = []
sd_list = []

csv_files = get_csv_files()
#print(csv_files)

#extarct information from filename
name, first_date, last_date, files_sorted = extract_name_date(csv_files)

filename_daily = f'{name}_{first_date}_to_{last_date}_daily.csv' #file for range of dates for daily metrics
check_file_exists(filename_daily)
filename_5min_window = f'{name}_{first_date}_to_{last_date}_5min.csv' #file for range of dates for daily metrics
check_file_exists(filename_5min_window)

for file in files_sorted:
    vlf_list = []
    total_power_list = []
    si_sleep = []
    
    current_date = file[2]
    current_date = current_date[:4] + '-' + current_date[4:6] + '-' + current_date[6:]
    file = '.'.join(file)
    data = pd.read_csv(file)
    
    df_hrv = find_peaks_and_scale(data)

    hrv_range = create_time_intervals(NUM_MINUTES_WINDOW, df_hrv)

    for n in range(len(hrv_range)-1):
        #Caluclates values over window range for short term recovery
        si_df = df_hrv.loc[df_hrv['ts'] < hrv_range[n+1]]
        #print(len(si_df), "---")
        si_df = si_df.loc[si_df['ts'] > hrv_range[n]]
        #print(len(si_df), "+++")
        si_np = si_df['hrv'].to_numpy()
        si_np = si_np*1000

        si_df_interpolated_nn_intervals = process_rr_nn_intervals(si_np)
        
        if si_df_interpolated_nn_intervals == 0:
            si_values.append(0)
            time_list.append(hrv_range[n+1])
            lf_hf_list.append(0)
            #vlf_list.append(0)
            #total_power_list.append(0)
            continue

        si = calculate_si(si_df_interpolated_nn_intervals)
        #print(time_list)
        try:
           freq_measures = get_frequency_domain_features(si_df_interpolated_nn_intervals, method='lomb')
           #print('Y', freq_measures['lf_hf_ratio'])
        except:
            lf_hf_list.append(0)
            

        
        si_values.append(si)
        time_list.append(hrv_range[n+1])
        lf_hf_list.append(freq_measures['lf_hf_ratio'])



    si_values_np = np.array(si_values)
    si_diff_np = np.diff(si_values_np)
    time_values_np = np.array(time_list)
    time_diff_np = np.diff(time_values_np)
    si_diff = si_diff_np/time_diff_np
    si_diff = np.insert(si_diff, 0, 0)


    #print(len(si_values), len(lf_hf_list), len(si_diff), len(time_list))
    metrics_dict = {'si_values': si_values, 'lf_hf_list':lf_hf_list, 'si_diff':si_diff, 'timestamp': time_list}
    try:
        # If the DataFrame exists, append the dictionary to it
        metrics_5min_df = pd.concat([metrics_5min_df, pd.DataFrame.from_dict(metrics_dict)])
    except NameError:
        # If the DataFrame doesn't exist, create it and assign it the dictionary
        metrics_5min_df = pd.DataFrame.from_dict(metrics_dict)
        
    #Calculate overnight values to show slow recovery
    si_np = df_hrv['hrv'].to_numpy()
    si_np = si_np*1000
    si_df_interpolated_nn_intervals = process_rr_nn_intervals(si_np)
    if si_df_interpolated_nn_intervals == 0:
        si_sleep.append(0)
        #time_list.append(hrv_range[n+1])
        vlf_list.append(0)
        total_power_list.append(0)
        sd_list.append([0, 0, 0])
        continue
    sd_info = get_poincare_plot_features(si_df_interpolated_nn_intervals)
    si = calculate_si(si_df_interpolated_nn_intervals)
    try:
        freq_measures = get_frequency_domain_features(si_df_interpolated_nn_intervals, method='lomb')
    except:
        vlf_list.append(0)
        total_power_list.append(0)
    #freq_measures = get_frequency_domain_features(si_df_interpolated_nn_intervals, method='lomb')

    si_sleep.append(si)
    vlf_list.append(freq_measures['vlf'])
    total_power_list.append(freq_measures['total_power'])
    sd_list.append([sd_info['sd1'], sd_info['sd2'], sd_info['ratio_sd2_sd1']])
    try:
        vlf_percent = vlf_list[0]/total_power_list[0]
    except ZeroDivisionError:
        vlf_percent = 0

    daily_metrics_dict = {'si_values': si_sleep, 'vlf_list':vlf_list, 'total_power':total_power_list, 'vlf/tp': vlf_percent, 'date': current_date}
    try:
        # If the DataFrame exists, append the dictionary to it
        metrics_daily_df = pd.concat([metrics_daily_df, pd.DataFrame.from_dict(daily_metrics_dict)])
    except NameError:
        # If the DataFrame doesn't exist, create it and assign it the dictionary
        metrics_daily_df = pd.DataFrame.from_dict(daily_metrics_dict)


#print(len(metrics_5min_df))
#print(len(metrics_daily_df))
metrics_daily_df.to_csv(filename_daily, index=False)
metrics_5min_df.to_csv(filename_5min_window, index=False)




    