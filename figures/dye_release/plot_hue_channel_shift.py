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

    all_hist_hue = []
    all_hist_position = []
    for hue_file in hue_files:
        results = read_from_json(hue_file)
        all_hist_hue.append(results['hist_hue'][0:last_index])
        all_hist_position.append(results['hist_position'][0:last_index])

    info = {}
    info['hist_hue'] = np.array(all_hist_hue)
    info['hist_position'] = np.array(all_hist_position)
    return info

if __name__ == '__main__':

    HUE_THRESHOLD = 80
    LAST_INDEX = 5980

    DATA_PATH = os.path.join(HERE_PATH, 'data')

    COLD_XP_PATH = os.path.join(DATA_PATH, 'AC_19.0_LJP5-22-Ey')
    cold_info = get_all_info_in_folder(COLD_XP_PATH, LAST_INDEX)

    HOT_XP_PATH = os.path.join(DATA_PATH, 'AC_28_LJP5-22-Ey')
    hot_info = get_all_info_in_folder(HOT_XP_PATH, LAST_INDEX)

    ##
    plot_folder = os.path.join(HERE_PATH, 'plot', 'hue_channel')
    filetools.ensure_dir(plot_folder)

    ## dye plot
    def plot_hue_diff(info, repeat_id):
        fig = plt.figure(figsize=(12, 8))
        with sns.axes_style("ticks"):
            ax = plt.subplot(111)

        plt.plot(info['hist_position'][repeat_id,0,:], info['hist_hue'][repeat_id,0,:], linewidth=3)
        plt.plot(info['hist_position'][repeat_id,LAST_INDEX-1,:], info['hist_hue'][repeat_id,LAST_INDEX-1,:], linewidth=3)
        plt.plot([HUE_THRESHOLD, HUE_THRESHOLD], [0, np.max(info['hist_hue'][repeat_id,LAST_INDEX-1,:])], '--k', linewidth=3)

        plt.xlim([0, 160])

        plt.xlabel('Intensity of hue channel', fontsize=fontsize)
        plt.ylabel('Number of pixels', fontsize=fontsize)

        plt.legend(['t=0$s$', 't=300$s$'], fontsize=fontsize, loc=1)

        sns.despine(offset=0, trim=True, ax=ax)
        plt.tight_layout()

        return fig

    plt.ion()

    for i in range(20):
        fig = plot_hue_diff(cold_info, i)
        figure_filebasename = os.path.join(plot_folder, 'cold_{}'.format(i))
        save_and_close_fig(fig, figure_filebasename)

    for i in range(20):
        fig = plot_hue_diff(hot_info, i)
        figure_filebasename = os.path.join(plot_folder, 'hot_{}'.format(i))
        save_and_close_fig(fig, figure_filebasename)
