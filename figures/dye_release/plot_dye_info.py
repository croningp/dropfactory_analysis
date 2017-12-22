import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

from utils.tools import read_from_json

import numpy as np

import filetools

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})


def get_all_info_in_folder(path, last_index=5900):
    hue_files = filetools.list_files(path, ['dye_release_info.json'])

    all_mean_hue = []
    all_ratio_above_threshold = []
    for hue_file in hue_files:
        results = read_from_json(hue_file)
        all_mean_hue.append(results['mean_hue'][0:last_index])
        all_ratio_above_threshold.append(results['ratio_above_threshold'][0:last_index])

    info = {}
    info['mean_hue'] = np.array(all_mean_hue)
    info['ratio_above_threshold'] = np.array(all_ratio_above_threshold)
    return info


def prepare_error_data(x, data, shift, spacing):
    y = np.mean(data, axis=0)
    yerr = np.std(data, axis=0) / np.sqrt(data.shape[0])  ## standard error

    ind = np.arange(shift, y.size-1, spacing, dtype=int)
    y = y[ind]
    yerr = yerr[ind]
    x = x[ind]

    return x, y, yerr

if __name__ == '__main__':

    LAST_INDEX = 5980

    DATA_PATH = os.path.join(HERE_PATH, 'data')

    COLD_XP_PATH = os.path.join(DATA_PATH, 'AC_19.0_LJP5-22-Ey')
    cold_info = get_all_info_in_folder(COLD_XP_PATH, LAST_INDEX)

    HOT_XP_PATH = os.path.join(DATA_PATH, 'AC_28_LJP5-22-Ey')
    hot_info = get_all_info_in_folder(HOT_XP_PATH, LAST_INDEX)

    fps = 20.0
    time_steps_in_sec =  np.arange(0, LAST_INDEX/fps, 1/fps)

    # plt.plot(time_steps_in_sec, np.mean(cold_info['ratio_above_threshold'], axis=0), 'b')
    # plt.plot(time_steps_in_sec, np.mean(hot_info['ratio_above_threshold'], axis=0), 'r')

    #
    N_PLOT_POINTS = 20
    linewidth = 4

    handles = []

    data = cold_info['ratio_above_threshold']
    x, y, yerr = prepare_error_data(time_steps_in_sec, data, 0, 20*fps)
    handle = plt.errorbar(x, y, yerr=yerr, linewidth=linewidth, color='b')
    handles.append(handle)


    data = hot_info['ratio_above_threshold']
    x, y, yerr = prepare_error_data(time_steps_in_sec, data, 0, 20*fps)
    handle = plt.errorbar(x, y, yerr=yerr, linewidth=linewidth, color='r')
    handles.append(handle)

    plt.xlim([-10, 300])
    plt.ylim([0, 1])

    plt.xlabel('Time - $s$', fontsize=fontsize)
    plt.ylabel('Ratio of Dyed Pixels', fontsize=fontsize)

    plt.legend(['19 C', '28 C'], fontsize=fontsize, loc=4)

    plt.tight_layout()
