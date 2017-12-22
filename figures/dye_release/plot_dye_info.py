import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

from utils.tools import read_from_json
from utils.plotting import save_and_close_fig

import numpy as np

import filetools

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 34
linewidth = 4
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


def get_all_temperature_in_folder(path):
    hue_files = filetools.list_files(path, ['temperature.json'])
    all_temperature = []
    for hue_file in hue_files:
        info = read_from_json(hue_file)
        all_temperature.append(info['temperature'])
    return all_temperature


def prepare_error_data(x, data, n_step_point):
    y = np.mean(data, axis=0)
    yerr = np.std(data, axis=0) / np.sqrt(data.shape[0])  ## standard error

    ind = np.linspace(0, y.size-1, n_step_point, dtype=int)
    y = y[ind]
    yerr = yerr[ind]
    x = x[ind]

    return x, y, yerr

if __name__ == '__main__':

    LAST_INDEX = 5980
    FPS = 20.0
    time_steps_in_sec =  np.arange(0, LAST_INDEX/FPS, 1/FPS)


    DATA_PATH = os.path.join(HERE_PATH, 'data')

    COLD_XP_PATH = os.path.join(DATA_PATH, 'AC_19.0_LJP5-22-Ey')
    cold_info = get_all_info_in_folder(COLD_XP_PATH, LAST_INDEX)
    cold_temperature = get_all_temperature_in_folder(COLD_XP_PATH)

    HOT_XP_PATH = os.path.join(DATA_PATH, 'AC_28_LJP5-22-Ey')
    hot_info = get_all_info_in_folder(HOT_XP_PATH, LAST_INDEX)
    hot_temperature = get_all_temperature_in_folder(HOT_XP_PATH)

    ##

    ##
    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    color_palette = sns.diverging_palette(145, 280, s=85, l=25, n=2)
    cold_color = color_palette[0]
    hot_color = color_palette[1]

    mean_cold_temperature = round(np.mean(cold_temperature), 1)
    std_cold_temperature = round(np.std(cold_temperature), 1)
    cold_label = 'T = {}$\pm${} {}'.format(mean_cold_temperature, std_cold_temperature, '${^o}C$')

    mean_hot_temperature = round(np.mean(hot_temperature), 1)
    std_hot_temperature = round(np.std(hot_temperature), 1)
    hot_label = 'T = {}$\pm${} {}'.format(mean_hot_temperature, std_hot_temperature, '${^o}C$')

    ## dye plot
    fig = plt.figure(figsize=(8, 8))
    with sns.axes_style("ticks"):
        ax = plt.subplot(111)

    N_STEP_POINT = 20

    handles = []

    data = cold_info['ratio_above_threshold']
    x, y, yerr = prepare_error_data(time_steps_in_sec, data, N_STEP_POINT)
    handle = plt.errorbar(x, y, yerr=yerr, linewidth=linewidth, color=cold_color)
    handles.append(handle)

    data = hot_info['ratio_above_threshold']
    x, y, yerr = prepare_error_data(time_steps_in_sec, data, N_STEP_POINT)
    handle = plt.errorbar(x, y, yerr=yerr, linewidth=linewidth, color=hot_color)
    handles.append(handle)

    plt.xlim([-10, 300])
    plt.ylim([0, 1.1])

    plt.xlabel('Time / $s$', fontsize=fontsize)
    plt.ylabel('Ratio of Dyed Pixels', fontsize=fontsize)

    plt.legend([cold_label, hot_label], fontsize=fontsize, loc=2)

    sns.despine(offset=0, trim=True, ax=ax)
    plt.tight_layout()

    figure_filebasename = os.path.join(plot_folder, 'dye_release')
    save_and_close_fig(fig, figure_filebasename)

    ##
    fig = plt.figure(figsize=(8, 8))
    with sns.axes_style("ticks"):
        ax = plt.subplot(111)

    plt.scatter(range(len(cold_temperature)), cold_temperature, linewidth=linewidth, color=cold_color)
    plt.scatter(range(len(hot_temperature)), hot_temperature, linewidth=linewidth, color=hot_color)

    plt.xlim([-1, 21])
    plt.ylim([15, 30])

    plt.xlabel('Experiment Number', fontsize=fontsize)
    plt.ylabel('Temperature / ${^o}C$', fontsize=fontsize)

    legend = plt.legend([cold_label, hot_label], fontsize=fontsize, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

    sns.despine(offset=0, trim=True, ax=ax)
    plt.tight_layout()

    figure_filebasename = os.path.join(plot_folder, 'temperatures')
    save_and_close_fig(fig, figure_filebasename, legend=legend)
