import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '../..')
sys.path.append(root_path)

import numpy as np
import scipy

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})

linewidth = 4
helpers_linewidth = 2

import filetools
from utils.tools import read_from_json
from utils.plotting import save_and_close_fig

METHOD_NAMES = ['random_params', 'random_goal']
SEEDS = ['110', '111', '112']

if __name__ == '__main__':

    data_folder = os.path.join(HERE_PATH, 'data')
    datafilename = os.path.join(data_folder, 'concave_hulls.json')
    coverage_data = read_from_json(datafilename)

    ##
    plot_folder = os.path.join(HERE_PATH, 'plot_concave')
    filetools.ensure_dir(plot_folder)

    plt.ion()

    ##
    fig = plt.figure(figsize=(10, 8))

    legend_names = []
    for i_method_name, method_name in enumerate(METHOD_NAMES):
        for i_seed, seed in enumerate(SEEDS):

            cov = np.array(coverage_data[method_name][seed])
            cov = cov / coverage_data['global_coverage']
            plt.plot(cov, linewidth=linewidth)

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
    ax = plt.subplot(111)

    color_palette = sns.color_palette("Paired")
    COLORS = [color_palette[1], color_palette[5]]

    mean_coverage_data = {}
    std_coverage_data = {}
    final_coverage = {}
    for i_method_name, method_name in enumerate(METHOD_NAMES):
        coverages = []
        final_coverage[method_name] = []
        for i_seed, seed in enumerate(SEEDS):
            cov = np.array(coverage_data[method_name][seed])
            cov = cov / coverage_data['global_coverage']
            cov_percent = 100 * cov
            coverages.append(cov_percent)
            final_coverage[method_name].append(cov_percent[-1])

        mean_coverage_data[method_name] = np.mean(coverages, axis=0)
        std_coverage_data[method_name] = np.std(coverages, axis=0)

        print '###'
        print method_name
        print 'mean {}'.format(np.mean(coverages, axis=0)[-1])
        print 'std {}'.format(np.std(coverages, axis=0)[-1])

        sns.tsplot(coverages, color=COLORS[i_method_name], linewidth=linewidth)

    print '###'
    print scipy.stats.ttest_ind(final_coverage['random_params'], final_coverage['random_goal'], equal_var=False)

    final_coverage_random_params = mean_coverage_data['random_params'][-1]
    final_coverage_random_goal = mean_coverage_data['random_goal'][-1]

    index_above_final_coverage_random_params = np.where(np.array(mean_coverage_data['random_goal']) > final_coverage_random_params)
    intersection_iteration = index_above_final_coverage_random_params[0][0] + 1 # index starts at 0, iteration number at 1

    line_color = sns.xkcd_palette(['slate grey'])[0]
    ax.plot([0, 1000], [final_coverage_random_params, final_coverage_random_params], c=line_color, linewidth=helpers_linewidth, linestyle='--')
    ax.plot([0, 1000], [final_coverage_random_goal, final_coverage_random_goal], c=line_color, linewidth=helpers_linewidth, linestyle='--')
    ax.plot([intersection_iteration, intersection_iteration], [0, final_coverage_random_params], c=line_color, linewidth=helpers_linewidth, linestyle='--')

    xticks = np.sort([0, 500, 1000, intersection_iteration])
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks)

    yticks = np.sort([0, final_coverage_random_params, 50, final_coverage_random_goal, 100])
    ax.set_yticks(yticks)
    ax.set_yticklabels(['{:.0f} %'.format(ytick) for ytick in yticks])

    plt.xlim([0, 1020])
    plt.ylim([0, 100])

    plt.xlabel('Number of experiments', fontsize=fontsize)
    plt.ylabel('% Explored', fontsize=fontsize)
    plt.legend(METHOD_NAMES, fontsize=fontsize, loc=2)

    sns.despine(offset=10, trim=True, ax=ax)
    plt.tight_layout()

    figure_filebasename = os.path.join(plot_folder, 'mean_coverages')
    save_and_close_fig(fig, figure_filebasename)
