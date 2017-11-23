import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '../..')
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

LEGEND_NAMES = ['Random Screening', 'Goal Babbling']
X_FEATURE_NAME = 'Number of experiments'
Y_FEATURE_NAME = 'Average Exploration / $AU$'

color_palette = sns.color_palette("Paired")
COLORS = [color_palette[1], color_palette[5]]

if __name__ == '__main__':

    data_folder = os.path.join(HERE_PATH, 'data')
    datafilename = os.path.join(data_folder, 'coverages.json')
    coverage_data = read_from_json(datafilename)

    ##
    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    ##
    fig = plt.figure(figsize=(10, 8))

    legend_names = []
    for i_method_name, method_name in enumerate(METHOD_NAMES):
        for i_seed, seed in enumerate(SEEDS):

            plt.plot(coverage_data[method_name][seed], linewidth=3)

            legend_names.append('{}_{}'.format(method_name, seed))

    plt.xlabel(X_FEATURE_NAME, fontsize=fontsize)
    plt.ylabel(Y_FEATURE_NAME, fontsize=fontsize)
    legend = plt.legend(legend_names, fontsize=26, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.tight_layout()

    figure_filebasename = os.path.join(plot_folder, 'all_coverages')
    save_and_close_fig(fig, figure_filebasename, legend=legend)

    ##
    fig = plt.figure(figsize=(12, 8))

    # with sns.axes_style("ticks"):
    #     ax1 = plt.subplot(111)

    split = 10 ## for no logical reasons 100 breaks it but make it work nicer
    with sns.axes_style("ticks"):
        ax1 = plt.subplot2grid((1, split), (0, 0), colspan=split-1)
    with sns.axes_style("white"):
        ax2 = plt.subplot2grid((1, split), (0, split-1), colspan=1)

    ## finding intersectiong
    final_coverage_random_params = coverage_data['random_params']['mean'][-1]
    final_coverage_random_goal = coverage_data['random_goal']['mean'][-1]

    index_above_final_coverage_random_params = np.where(np.array(coverage_data['random_goal']['mean']) > final_coverage_random_params)
    intersection_iteration = index_above_final_coverage_random_params[0][0] + 1 # index starts at 0, iteration number at 1

    line_color = sns.xkcd_palette(['slate grey'])[0]
    ax1.plot([0, 1000], [final_coverage_random_params, final_coverage_random_params], c=line_color, linewidth=1, linestyle='--')
    ax1.plot([0, 1000], [final_coverage_random_goal, final_coverage_random_goal], c=line_color, linewidth=1, linestyle='--')
    ax1.plot([intersection_iteration, intersection_iteration], [0, final_coverage_random_params], c=line_color, linewidth=1, linestyle='--')

    xticks = np.sort([0, 500, 1000, intersection_iteration])
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xticks)

    yticks = np.sort([0.0, final_coverage_random_params, final_coverage_random_goal])
    ax1.set_yticks(yticks)
    ax1.set_yticklabels(['{0:.2f}'.format(ytick) for ytick in yticks])

    #
    handles = []
    for i_method_name, method_name in enumerate(METHOD_NAMES):
        y = np.array(coverage_data[method_name]['mean'])
        yerr = np.array(coverage_data[method_name]['std'])
        x = np.array(range(y.size)) + 1

        ind = np.linspace(0, y.size-1, 11, dtype=int)
        y = y[ind]
        yerr = yerr[ind]
        x = x[ind]

        #
        coverages = []
        for i_seed, seed in enumerate(SEEDS):
            coverages.append(coverage_data[method_name][seed])


        # handle = sns.tsplot(data=coverages, err_style="ci_band", ci=[95], ax=ax1, linewidth=3, color=COLORS[i_method_name])
        handle = ax1.errorbar(x, y, yerr=yerr, linewidth=3, color=COLORS[i_method_name])
        handles.append(handle)


        sns.boxplot(data=np.array(coverages)[:,-1], color=COLORS[i_method_name], ax=ax2)

    ## ax1 nice
    ax1.set_xlim([0, 1020])
    ax1.set_ylim([0, 0.25])

    ax1.set_xlabel(X_FEATURE_NAME, fontsize=fontsize)
    ax1.set_ylabel(Y_FEATURE_NAME, fontsize=fontsize)
    ax1.legend(handles, LEGEND_NAMES, fontsize=fontsize, loc=2)

    sns.despine(offset=10, trim=True, ax=ax1)

    ## ax2 nice
    ax2.set_ylim([0, 0.25])

    ax2.set_yticks([])
    ax2.set_xticks([])
    ax2.set_yticklabels([])
    ax2.set_xticklabels([])

    sns.despine(left=True, bottom=True, ax=ax2)

    plt.tight_layout()

    figure_filebasename = os.path.join(plot_folder, 'mean_coverages')
    save_and_close_fig(fig, figure_filebasename)

    ##
