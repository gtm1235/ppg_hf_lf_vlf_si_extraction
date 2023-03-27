import pandas as pd
from scipy.signal import find_peaks
import numpy as np

def find_peaks_and_scale(data):
    peaks, heights_peak_0 = find_peaks(-data['red_filt'], distance=16)
    peaks_hrv = np.diff(peaks)
    peaks_hrv = peaks_hrv/48
    df_rf = data['ts'].apply(lambda x: int(x/1000000))
    df_rf = df_rf.iloc[peaks].iloc[1:]
    df_hrv = pd.DataFrame(data={'ts':df_rf, 'hrv':peaks_hrv})
    df_hrv.reset_index(drop=True)

    return df_hrv