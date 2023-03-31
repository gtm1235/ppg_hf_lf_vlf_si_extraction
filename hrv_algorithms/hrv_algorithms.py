import math
import pandas as pd
import numpy as np

from hrvanalysis import (
    remove_outliers,
    remove_ectopic_beats,
    interpolate_nan_values
)

from utils.utils import median_bin_count


def calculate_si(data):
    data = pd.DataFrame(data, columns=['hrv'])
    median = data['hrv'].median()
    hrv_max = max(data['hrv'])
    hrv_min = min(data['hrv'])

    if math.isnan(hrv_min) or math.isnan(hrv_max):
        return 0
    if hrv_max-hrv_min == 0:
        return 0
    
    bins_count = math.floor((hrv_max-hrv_min)/50)
    frq, edges = np.histogram(data, bins=bins_count)
    count = median_bin_count(edges, median)
    max_bin = frq[count-1]
    top = (max_bin/len(data))*100

    SI = (top/(2*median*(hrv_max-hrv_min)))*1000000
    return SI


def process_rr_nn_intervals(si_np):
    si_df_no_outliers = remove_outliers(
        rr_intervals=si_np, low_rri=400, high_rri=2000, verbose=False)
    si_df_interpolated_rr_intervals = interpolate_nan_values(rr_intervals=si_df_no_outliers,
                                                             interpolation_method="linear")
    
    if len(si_df_interpolated_rr_intervals) == 0:
        return 0

    si_df_nn_intervals_list = remove_ectopic_beats(
        rr_intervals=si_df_interpolated_rr_intervals, method="malik", verbose=False)
    si_df_interpolated_nn_intervals = interpolate_nan_values(
        rr_intervals=si_df_nn_intervals_list)

    if len(si_df_interpolated_nn_intervals) == 0:
        return 0
    elif np.isnan(si_df_interpolated_nn_intervals).any() == True:
        return 0
    else:
        return si_df_interpolated_nn_intervals
