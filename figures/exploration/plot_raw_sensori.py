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

import filetools
from utils.plotting import save_and_close_fig

# design figure
fontsize = 34
matplotlib.rc('xtick', labelsize=30)
matplotlib.rc('ytick', labelsize=30)
matplotlib.rcParams.update({'font.size': fontsize})

max_lim = 21.5

if __name__ == '__main__':

    X_FEATURE_NAME = 'average_speed'
    Y_FEATURE_NAME = 'average_number_of_droplets'

    X_LABEL = 'Droplet Speed / $mm.s^{-1}$'
    Y_LABEL = 'No. of Droplets'

    color_palette = sns.color_palette("Paired")
    COLORS = [color_palette[1], color_palette[5]]

    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    # we plot each subfigure independently and will join them in inkscape

    # random params, seed 112
    fig  = plt.figure(figsize=(8,8))
    with sns.axes_style("ticks"):
        ax = plt.subplot(111)

    data = load_dataset(forge_dataset_filename('random_params', '111'))
    x = data['droplet_features'][X_FEATURE_NAME]
    y = data['droplet_features'][Y_FEATURE_NAME]

    plt.scatter(x, y, 100, c=COLORS[0])
    plt.xlim([-1, max_lim])
    plt.ylim([-1, max_lim])
    plt.xlabel(X_LABEL, fontsize=fontsize)
    plt.ylabel(Y_LABEL, fontsize=fontsize)

    sns.despine(offset=0, trim=True, ax=ax)
    plt.tight_layout()

    figure_filebasename = os.path.join(plot_folder, 'random_params_111')
    save_and_close_fig(fig, figure_filebasename)

    # random goals, seed 112
    fig  = plt.figure(figsize=(8,8))
    with sns.axes_style("ticks"):
        ax = plt.subplot(111)

    data = load_dataset(forge_dataset_filename('random_goal', '111_speed_division'))
    x = data['droplet_features'][X_FEATURE_NAME]
    y = data['droplet_features'][Y_FEATURE_NAME]

    plt.scatter(x, y, 100, c=COLORS[1])

    plt.axis('scaled')

    plt.xlim([-1, max_lim])
    plt.ylim([-1, max_lim])
    plt.xlabel(X_LABEL, fontsize=fontsize)
    plt.ylabel(Y_LABEL, fontsize=fontsize)

    sns.despine(offset=0, trim=True, ax=ax)
    plt.tight_layout()

    figure_filebasename = os.path.join(plot_folder, 'random_goals_111')
    save_and_close_fig(fig, figure_filebasename)
