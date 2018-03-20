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

from statsmodels.nonparametric.kde import KDEUnivariate

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})

if __name__ == '__main__':

    X_FEATURE_NAME = 'average_speed'
    METHOD_NAMES = ['random_params', 'random_goal']
    SEED_HOT = ['110', '111', '112']
    SEED_COLD = ['210', '211', '212']
    SEEDS_SET = [SEED_HOT, SEED_COLD]
    SEEDS_SET_NAME = ['HOT', 'COLD']

    N_METHODS = len(METHOD_NAMES)

    #
    DATA = {}
    for i_method_name, method_name in enumerate(METHOD_NAMES):
        DATA[method_name] = {}
        for i_seed_set, seed_set_name in enumerate(SEEDS_SET_NAME):
            DATA[method_name][seed_set_name] = {}

            seed_set_speeds = []
            for i_seed, seed in enumerate(SEEDS_SET[i_seed_set]):
                dataset_seed = seed
                if method_name != 'random_params':
                    dataset_seed = '{}_speed_division'.format(seed)
                data = load_dataset(forge_dataset_filename(method_name, dataset_seed))

                speeds = np.array(data['droplet_features'][X_FEATURE_NAME])

                seed_set_speeds.append(speeds)

            data_fit = np.array(seed_set_speeds).ravel()

            kde = KDEUnivariate(data_fit)
            kde.fit()

            DATA[method_name][seed_set_name]['data_fit'] = data_fit
            DATA[method_name][seed_set_name]['support'] = kde.support
            DATA[method_name][seed_set_name]['density'] = kde.density
            DATA[method_name][seed_set_name]['cdf'] = kde.cdf
            DATA[method_name][seed_set_name]['inverse_cdf'] = 1 - kde.cdf

    ##
    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    color_palette = sns.color_palette("Paired")
    plt.ion()

    linewidth = 4

    ##
    fig = plt.figure(figsize=(16,8))
    ax = plt.subplot(111)

    plt.plot([-1, 21], [0, 0], 'k--')
    plt.plot(DATA['random_params']['COLD']['support'], DATA['random_params']['COLD']['density'], color=color_palette[0], linewidth=linewidth)
    plt.plot(DATA['random_params']['HOT']['support'], DATA['random_params']['HOT']['density'], color=color_palette[1], linewidth=linewidth)

    y_max = plt.ylim()[1]
    plt.xlim([0, 10])
    plt.ylim([-y_max/20, y_max])

    plt.title('Random Parameters', fontsize=fontsize)
    plt.xlabel('Droplet Speed / $mm.s^{-1}$')
    plt.ylabel('Probability Density')
    plt.legend(['0', '22 C', '26 C'])

    sns.despine(offset=0, trim=True, ax=ax)
    plt.tight_layout()

    figure_filebasename = os.path.join(plot_folder, 'probability_density_random_params')
    save_and_close_fig(fig, figure_filebasename)

    ##
    fig = plt.figure(figsize=(16,8))
    ax = plt.subplot(111)

    plt.plot([-1, 21], [0, 0], 'k--')
    plt.plot(DATA['random_goal']['COLD']['support'], DATA['random_goal']['COLD']['density'], color=color_palette[4], linewidth=linewidth)
    plt.plot(DATA['random_goal']['HOT']['support'], DATA['random_goal']['HOT']['density'], color=color_palette[5], linewidth=linewidth)

    y_max = plt.ylim()[1]
    plt.xlim([0, 10])
    plt.ylim([-y_max/20, y_max])

    plt.title('Goal Babbling', fontsize=fontsize)
    plt.xlabel('Droplet Speed / $mm.s^{-1}$')
    plt.ylabel('Probability Density')
    plt.legend(['0', '22 C', '26 C'])

    sns.despine(offset=0, trim=True, ax=ax)
    plt.tight_layout()

    figure_filebasename = os.path.join(plot_folder, 'probability_density_random_goal')
    save_and_close_fig(fig, figure_filebasename)
