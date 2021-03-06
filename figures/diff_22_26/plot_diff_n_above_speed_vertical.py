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

    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    #
    DATA = {}
    for i_method_name, method_name in enumerate(METHOD_NAMES):
        DATA[method_name] = {}
        for i_seed, seed in enumerate(SEEDS):
            DATA[method_name][seed] = {}

            dataset_seed = seed
            if method_name != 'random_params':
                dataset_seed = '{}_speed_division'.format(seed)
            data = load_dataset(forge_dataset_filename(method_name, dataset_seed))

            x = np.array(data['droplet_features'][X_FEATURE_NAME])
            y = np.array(data['droplet_features'][Y_FEATURE_NAME])
            temperatures = np.array(data['xp_info']['temperature'])

            DATA[method_name][seed][X_FEATURE_NAME] = x
            DATA[method_name][seed][Y_FEATURE_NAME] = y
            DATA[method_name][seed]['temperature'] = temperatures
            DATA[method_name][seed]['temperature_mean'] = temperatures[np.logical_not(np.equal(temperatures, None))].mean()
            DATA[method_name][seed]['temperature_std'] = temperatures[np.logical_not(np.equal(temperatures, None))].std()

            # plt.subplot(N_METHODS, N_SEEDS, i_method_name*N_SEEDS + i_seed + 1)
            # sns.distplot(x, bins=range(21))
            # plt.title()

    ##
    SEEDS_26 = ['110', '111', '112']
    SEEDS_22 = ['210', '211', '212']

    THRESHOLD = 3

    RESULTS = {}
    for i_method_name, method_name in enumerate(METHOD_NAMES):

        RESULTS[method_name] = {}

        n_observation_above = []
        for seed in SEEDS_26:
            n_observation_above.append(np.sum(DATA[method_name][seed][X_FEATURE_NAME] >= THRESHOLD))
        RESULTS[method_name]['NB_26'] = n_observation_above

        n_observation_above = []
        for seed in SEEDS_22:
            n_observation_above.append(np.sum(DATA[method_name][seed][X_FEATURE_NAME] >= THRESHOLD))
        RESULTS[method_name]['NB_22'] = n_observation_above


        temperatures = []
        for seed in SEEDS_26:
            temperatures.append(DATA[method_name][seed]['temperature_mean'])
        RESULTS[method_name]['TEMP_26'] = temperatures

        temperatures = []
        for seed in SEEDS_22:
            temperatures.append(DATA[method_name][seed]['temperature_mean'])
        RESULTS[method_name]['TEMP_22'] = temperatures


    ##
    import scipy
    print 'random 22: mean {} / std {}'.format(np.mean(RESULTS['random_params']['NB_22']), np.std(RESULTS['random_params']['NB_22']))
    print 'random 26: mean {} / std {}'.format(np.mean(RESULTS['random_params']['NB_26']), np.std(RESULTS['random_params']['NB_26']))
    print 'goal babbling 22: mean {} / std {}'.format(np.mean(RESULTS['random_goal']['NB_22']), np.std(RESULTS['random_goal']['NB_22']))
    print 'goal babbling 26: mean {} / std {}'.format(np.mean(RESULTS['random_goal']['NB_26']), np.std(RESULTS['random_goal']['NB_26']))

    print '### random 22 vs random 26'
    print scipy.stats.ttest_ind(RESULTS['random_params']['NB_22'], RESULTS['random_params']['NB_26'], equal_var=False)
    print '### goal babbling 22 vs goal babbling 26'
    print scipy.stats.ttest_ind(RESULTS['random_goal']['NB_22'], RESULTS['random_goal']['NB_26'], equal_var=False)
    print '### random 22 vs goal babbling 22'
    print scipy.stats.ttest_ind(RESULTS['random_params']['NB_22'], RESULTS['random_goal']['NB_22'], equal_var=False)
    print '### random 26 vs goal babbling 26'
    print scipy.stats.ttest_ind(RESULTS['random_params']['NB_26'], RESULTS['random_goal']['NB_26'], equal_var=False)


    ##
    BAR_WIDTH = 0.35       # the width of the bars

    fig = plt.figure(figsize=(8, 16))
    with sns.axes_style("ticks"):
        ax = plt.subplot(111)

    def plot_rect(ax, pos, data, color):
        err_color = sns.xkcd_palette(['slate grey'])[0]
        return ax.bar(pos, np.mean(data), BAR_WIDTH, color=color, yerr=np.std(data), error_kw=dict(ecolor=err_color, lw=2, capsize=5, capthick=2))

    color_palette = sns.color_palette("Paired")
    rects1 = plot_rect(ax, 2, RESULTS['random_params']['NB_22'], color_palette[0])
    rects2 = plot_rect(ax, 2-BAR_WIDTH, RESULTS['random_params']['NB_26'], color_palette[1])
    rects3 = plot_rect(ax, 1, RESULTS['random_goal']['NB_22'], color_palette[4])
    rects4 = plot_rect(ax, 1-BAR_WIDTH, RESULTS['random_goal']['NB_26'], color_palette[5])

    y_ticks_value = []
    y_ticks_value.append(0)
    y_ticks_value.append(np.mean(RESULTS['random_params']['NB_22']))
    y_ticks_value.append(np.mean(RESULTS['random_params']['NB_26']))
    y_ticks_value.append(np.mean(RESULTS['random_goal']['NB_22']))
    y_ticks_value.append(np.mean(RESULTS['random_goal']['NB_26']))

    ax.set_yticks(y_ticks_value)
    ax.set_yticklabels([str(int(y)) for y in y_ticks_value])

    ax.set_xticks([1, 2])
    ax.set_xticklabels(['Goal Babbling', 'Random Experiments'])

    # ax.set_xlim([BAR_WIDTH, 2+BAR_WIDTH])
    # ax.set_ylim([0, 350])

    t = 'No. of experiments with droplet speed > {} {}'.format(THRESHOLD, '$mm.s^{-1}$')
    ax.set_ylabel(t, fontsize=fontsize)

    sns.despine(offset=20, trim=True, left=True, ax=ax)
    plt.tight_layout()


    figure_filebasename = os.path.join(plot_folder, 'diff_22_26_n_above_speed_vertical')
    save_and_close_fig(fig, figure_filebasename)
