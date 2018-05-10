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
fontsize = 34
matplotlib.rc('xtick', labelsize=30)
matplotlib.rc('ytick', labelsize=30)
matplotlib.rcParams.update({'font.size': fontsize})


import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from utils.plotting import plot_kde
from utils.exploration import compute_explored_volume
from utils.exploration import compute_volume_concave_hull


X_FEATURE_NAME = 'average_speed'
Y_FEATURE_NAME = 'average_number_of_droplets'

X_FEATURE_LABEL = 'Droplet Speed / $mm.s^{-1}$'
Y_FEATURE_LABEL = 'No. of Droplets'

MIN_FEATURE_LIM = -1.5
MAX_FEATURE_LIM = 21.5


from utils.plotting import save_and_close_fig

import plot_tools

def init_single_fig_ax():
    fig  = plt.figure(figsize=(8,8))
    with sns.axes_style("ticks"):
        ax = plt.subplot(111)
    return fig, ax

def save_it(fig, plot_folder, filebasename):

    for ext in ['.png']:
    # for ext in ['.png', '.eps', '.svg']:
        plot_dir = os.path.join(plot_folder, ext[1:])
        filetools.ensure_dir(plot_dir)

        figure_filebasename = os.path.join(plot_dir, filebasename)

        save_and_close_fig(fig, figure_filebasename, exts=[ext])


def plot_it_all(data, plot_folder, stepping=10, color='b'):

    for up_to_iteration in range(stepping, 1000+stepping, stepping):
        ## exploration
        fig, ax = init_single_fig_ax()
        plot_raw_exploration(ax, data, up_to_iteration, color=color)
        ax.set_title('$t={:04d}$'.format(up_to_iteration), fontsize=fontsize)
        save_it(fig, plot_folder, 'exploration_raw_{:04d}'.format(up_to_iteration))

    ##
    fig  = plt.figure(figsize=(5*8,2*8))
    characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    for i in range(10):
        up_to_iteration = 100*(i+1)
        with sns.axes_style("ticks"):
            ax = plt.subplot(2,5,i+1)
        plot_raw_exploration(ax, data, up_to_iteration, color=color)
        ax.set_title('$t={}$'.format(up_to_iteration), fontsize=fontsize)
        # plt.text(10,15,'$t={}$'.format(up_to_iteration))
        plt.text(18,19,'({})'.format(characters[i]))

    plt.tight_layout()
    save_it(fig, plot_folder, 'exploration_pannel')


def plot_raw_exploration(ax, data, up_to_iteration, color='b'):

    x = data['droplet_features'][X_FEATURE_NAME]
    y = data['droplet_features'][Y_FEATURE_NAME]

    ax.scatter(x[:up_to_iteration], y[:up_to_iteration], 100, c=color)
    ax.scatter(x[up_to_iteration-1], y[up_to_iteration-1], 100, c='k')

    ax.axis('scaled')

    ax.set_xlim([MIN_FEATURE_LIM, MAX_FEATURE_LIM])
    ax.set_ylim([MIN_FEATURE_LIM, MAX_FEATURE_LIM])
    ax.set_xlabel(X_FEATURE_LABEL, fontsize=fontsize)
    ax.set_ylabel(Y_FEATURE_LABEL, fontsize=fontsize)

    ax.set_title('Observations', fontsize=fontsize)

    plt.tight_layout()

if __name__ == '__main__':

    import filetools

    from datasets.datasets_tools import load_dataset
    from datasets.datasets_tools import forge_dataset_filename
    from datasets.datasets_tools import get_dataset_basepath

    dataset_path = get_dataset_basepath()
    plot_path = os.path.join(HERE_PATH, 'plot', 'scatter_interval_per_run')

    color_palette = sns.color_palette("Paired")
    random_params_color_cold = color_palette[0]
    random_params_color_hot = color_palette[1]
    random_goal_color_cold =  color_palette[4]
    random_goal_color_hot =  color_palette[5]

    flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
    color_palette = sns.color_palette(flatui)
    default_color = color_palette[4]

    STEPPING = 1

    data_files = filetools.list_files(dataset_path, 'data.json')
    for data_file in data_files:
        print data_file
        data = load_dataset(data_file)
        if len(data['paths']) == 1000:
            plot_folder = os.path.split(data_file)[0].replace(dataset_path, plot_path)

            if 'random_goal' in plot_folder:
                if '/1' in plot_folder:
                    color = random_goal_color_hot
                else:
                    color = random_goal_color_cold
            elif 'random_params' in plot_folder:
                if '/1' in plot_folder:
                    color = random_params_color_hot
                else:
                    color = random_params_color_cold
            else:
                color = default_color

            plot_it_all(data, plot_folder, STEPPING, color)
