import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '../../..')
sys.path.append(root_path)

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})

import filetools
from utils.tools import read_from_json
from utils.plotting import save_and_close_fig

METHOD_NAMES = ['random_params', 'random_goal']
SEEDS = ['110', '111', '112']

if __name__ == '__main__':

    data_folder = os.path.join(HERE_PATH, 'data')
    datafilename = os.path.join(data_folder, 'convex_hulls.json')
    coverage_data = read_from_json(datafilename)

    ##
    plot_folder = os.path.join(HERE_PATH, 'plot_convex')
    filetools.ensure_dir(plot_folder)

    ##
    fig = plt.figure(figsize=(10, 8))

    legend_names = []
    for i_method_name, method_name in enumerate(METHOD_NAMES):
        for i_seed, seed in enumerate(SEEDS):

            cov = np.array(coverage_data[method_name][seed])
            cov = cov / coverage_data['global_coverage']
            plt.plot(cov, linewidth=3)

            legend_names.append('{} {}'.format(method_name, seed))

    plt.ylim([0, 1])
    plt.xlabel('Iterations', fontsize=fontsize)
    plt.ylabel('% Explored', fontsize=fontsize)
    legend = plt.legend(legend_names, fontsize=26, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.tight_layout()

    figure_filebasename = os.path.join(plot_folder, 'all_coverages')
    save_and_close_fig(fig, figure_filebasename, legend=legend)

    ##
    fig = plt.figure(figsize=(10, 8))

    legend_names = []
    for i_method_name, method_name in enumerate(METHOD_NAMES):
        coverages = []
        for i_seed, seed in enumerate(SEEDS):
            cov = np.array(coverage_data[method_name][seed])
            cov = cov / coverage_data['global_coverage']
            coverages.append(cov)

        y = np.mean(coverages, 0)
        yerr = np.std(coverages, 0)
        x = np.array(range(y.size)) + 1

        ind = np.linspace(0, y.size-1, 11, dtype=int)
        y = y[ind]
        yerr = yerr[ind]
        x = x[ind]

        plt.errorbar(x, y, yerr=yerr, linewidth=3)

    plt.xlim([0, 1020])
    plt.ylim([0, 1])

    plt.xlabel('Iterations', fontsize=fontsize)
    plt.ylabel('Explored Area', fontsize=fontsize)
    plt.legend(METHOD_NAMES, fontsize=fontsize, loc=2)
    plt.tight_layout()

    figure_filebasename = os.path.join(plot_folder, 'mean_coverages')
    save_and_close_fig(fig, figure_filebasename)
