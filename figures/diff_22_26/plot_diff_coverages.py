import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '../..')
sys.path.append(root_path)

from datasets.datasets_tools import load_dataset
from datasets.datasets_tools import forge_dataset_filename

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np

import filetools
from utils.tools import read_from_json
from utils.plotting import save_and_close_fig

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})

if __name__ == '__main__':

    X_FEATURE_NAME = 'average_speed'
    Y_FEATURE_NAME = 'average_number_of_droplets'

    METHOD_NAMES = ['random_params', 'random_goal']
    SEEDS = ['110', '111', '112', '210', '211', '212']

    N_METHODS = len(METHOD_NAMES)
    N_SEEDS = len(SEEDS)

    data_folder = os.path.join(HERE_PATH, 'data')
    datafilename = os.path.join(data_folder, 'coverages.json')
    coverage_data = read_from_json(datafilename)

    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    ##
    SEEDS_26 = ['110', '111', '112']
    SEEDS_22 = ['210', '211', '212']

    RESULTS = {}
    for i_method_name, method_name in enumerate(METHOD_NAMES):

        RESULTS[method_name] = {}

        n_observation_above = []
        for seed in SEEDS_26:
            n_observation_above.append(coverage_data[method_name][seed][-1])
        RESULTS[method_name]['NB_26'] = n_observation_above

        n_observation_above = []
        for seed in SEEDS_22:
            n_observation_above.append(coverage_data[method_name][seed][-1])
        RESULTS[method_name]['NB_22'] = n_observation_above

    ##
    BAR_WIDTH = 0.35       # the width of the bars

    fig = plt.figure(figsize=(16, 8))
    with sns.axes_style("ticks"):
        ax = plt.subplot(111)

    def plot_rect(ax, pos, data, color):
        err_color = sns.xkcd_palette(['slate grey'])[0]
        return ax.barh(pos, np.mean(data), BAR_WIDTH, color=color, xerr=np.std(data), error_kw=dict(ecolor=err_color, lw=2, capsize=5, capthick=2))

    color_palette = sns.color_palette("Paired")
    rects1 = plot_rect(ax, 2, RESULTS['random_params']['NB_22'], color_palette[0])
    rects2 = plot_rect(ax, 2-BAR_WIDTH, RESULTS['random_params']['NB_26'], color_palette[1])
    rects3 = plot_rect(ax, 1, RESULTS['random_goal']['NB_22'], color_palette[4])
    rects4 = plot_rect(ax, 1-BAR_WIDTH, RESULTS['random_goal']['NB_26'], color_palette[5])

    x_ticks_value = []
    x_ticks_value.append(0)
    x_ticks_value.append(np.mean(RESULTS['random_params']['NB_22']+RESULTS['random_params']['NB_26']))
    # x_ticks_value.append(np.mean(RESULTS['random_params']['NB_26']))
    x_ticks_value.append(np.mean(RESULTS['random_goal']['NB_22']))
    x_ticks_value.append(np.mean(RESULTS['random_goal']['NB_26']))

    x_ticks_value = [round(x, 2) for x in x_ticks_value]

    ax.set_xticks(x_ticks_value)
    ax.set_xticklabels([str(x) for x in x_ticks_value])

    ax.set_yticks([1, 2])
    ax.set_yticklabels(['Goal Babbling', 'Random Experiments'])

    # ax.set_xlim([0, 350])
    ax.set_ylim([BAR_WIDTH, 2+BAR_WIDTH])

    t = '% Exploration'
    ax.set_xlabel(t, fontsize=fontsize)

    sns.despine(offset=20, trim=True, left=True, ax=ax)
    plt.tight_layout()


    figure_filebasename = os.path.join(plot_folder, 'diff_coverage_22_26')
    save_and_close_fig(fig, figure_filebasename)
