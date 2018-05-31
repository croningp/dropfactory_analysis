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
import scipy.signal

import filetools

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 34
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

# def prepare_smoothed_data(x, data, n_step_point, smooth_window=1001, polyorder=2):

def prepare_smoothed_data(x, data, n_step_point, p0, max_y):

    from scipy.optimize import curve_fit

    def sigmoid(x, x0, phi, min_y):
         y = (max_y - min_y) / (1 + np.exp(-(x-x0)/phi)) + min_y
         return y

    popt, pcov = curve_fit(sigmoid, x, np.mean(data, axis=0), p0=p0)
    y = sigmoid(x, *popt)

    ind = np.linspace(0, y.size-1, n_step_point, dtype=int)

    x = x[ind]
    y = y[ind]

    return x, y


if __name__ == '__main__':

    FPS = 20.0
    LAST_INDEX = int(270*FPS)

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
    plot_folder = os.path.join(HERE_PATH, 'plot', 'dye_timelaps_video')
    filetools.ensure_dir(plot_folder)

    color_palette = sns.diverging_palette(145, 280, s=85, l=25, n=2)
    cold_color = color_palette[0]
    hot_color = color_palette[1]

    mean_cold_temperature = round(np.mean(cold_temperature), 1)
    std_cold_temperature = round(np.std(cold_temperature), 1)
    cold_label = '{}$\pm${} {}'.format(mean_cold_temperature, std_cold_temperature, '${^o}C$')

    mean_hot_temperature = round(np.mean(hot_temperature), 1)
    std_hot_temperature = round(np.std(hot_temperature), 1)
    hot_label = '{}$\pm${} {}'.format(mean_hot_temperature, std_hot_temperature, '${^o}C$')


    def generate_plot_with_greenbar(greenbar_time=0):
        N_ERROR_POINT = 20
        N_SMOOTH_POINT = 240
        MARKER_SIZE = 15
        ELINEWIDTH = 2
        CAPTHICK = 2
        CAPSIZE = 2
        LINEWIDTH = 3
        SMOOTH_WINDOW = 1501
        MAX_Y = 0.73

        ## dye plot
        fig = plt.figure(figsize=(8, 8))
        with sns.axes_style("ticks"):
            ax = plt.subplot(111)

        handles = []

        ## hot
        data = hot_info['ratio_above_threshold']
        x, y, yerr = prepare_error_data(time_steps_in_sec, data, N_ERROR_POINT)
        plt.scatter(x, y, s=MARKER_SIZE, c=hot_color)
        handle = plt.errorbar(x, y, yerr=yerr, fmt='none', elinewidth=ELINEWIDTH, ecolor=hot_color, capsize=CAPSIZE)
        handles.append(handle)

        x, y = prepare_smoothed_data(time_steps_in_sec, data, N_SMOOTH_POINT, p0=[30, 20, 0], max_y=MAX_Y)
        plt.plot(x, y, c=hot_color, linewidth=LINEWIDTH)


        ## cold
        data = cold_info['ratio_above_threshold']
        x, y, yerr = prepare_error_data(time_steps_in_sec, data, N_ERROR_POINT)
        plt.scatter(x, y, s=MARKER_SIZE, c=cold_color)
        handle = plt.errorbar(x, y, yerr=yerr, fmt='none', elinewidth=ELINEWIDTH, ecolor=cold_color, capsize=CAPSIZE, capthick=CAPTHICK)
        handles.append(handle)

        x, y = prepare_smoothed_data(time_steps_in_sec, data, N_SMOOTH_POINT, p0=[150, 50, 0], max_y=MAX_Y)
        plt.plot(x, y, c=cold_color, linewidth=LINEWIDTH)

        ##

        plt.xlim([-10, 280])
        plt.xticks([0, 30, 60, 90, 120, 150, 180, 210, 240, 270], ('0', '', '60', '', '120', '', '180', '', '240', ''))

        plt.ylim([0, 1.1])

        plt.xlabel('Time / $s$', fontsize=fontsize)
        plt.ylabel('Ratio of Dyed Pixels', fontsize=fontsize)

        plt.legend([hot_label, cold_label], fontsize=fontsize-8, loc=9)

        plt.plot([greenbar_time, greenbar_time], [0, 0.8], c='r', linewidth=LINEWIDTH)

        sns.despine(offset=0, trim=True, ax=ax)
        plt.tight_layout()

        return fig

    ## video images

    iframe = 0

    SPEED_UP = 5
    OUT_VIDEO_FPS = 30
    N_REPEATED_FRAME = OUT_VIDEO_FPS/SPEED_UP

    for timestep in range(270):
        print timestep
        for _ in range(N_REPEATED_FRAME):
            fig = generate_plot_with_greenbar(greenbar_time=timestep)

            figure_filebasename = os.path.join(plot_folder, 'dye_release_smooth_{:04d}'.format(iframe))
            save_and_close_fig(fig, figure_filebasename, exts=['.png'])

            iframe += 1
