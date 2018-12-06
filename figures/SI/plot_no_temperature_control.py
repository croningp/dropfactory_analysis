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
fontsize = 36
small_fontsize = 30
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

def save_it(fig, plot_folder, filebasename, dpi=100):

    for ext in ['.png']:
    # for ext in ['.png', '.eps', '.svg']:
        plot_dir = os.path.join(plot_folder, ext[1:])
        filetools.ensure_dir(plot_dir)

        figure_filebasename = os.path.join(plot_dir, filebasename)

        save_and_close_fig(fig, figure_filebasename, exts=[ext], dpi=dpi)


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

    ax.set_xticks([0, 10, 20])
    ax.set_yticks([0, 10, 20])
    ax.set_xlabel(X_FEATURE_LABEL, fontsize=small_fontsize)
    ax.set_ylabel(Y_FEATURE_LABEL, fontsize=small_fontsize)
    # ax.set_title('Observations', fontsize=fontsize)

    # plt.tight_layout()

if __name__ == '__main__':

    import filetools

    from datasets.datasets_tools import load_dataset
    from datasets.datasets_tools import forge_dataset_filename
    from datasets.datasets_tools import get_dataset_basepath

    dataset_path = get_dataset_basepath()
    plot_path = os.path.join(HERE_PATH, 'plot', 'scatter_no_temperature_control')

    color_palette = sns.color_palette("Paired")
    random_params_color_cold = color_palette[0]
    random_params_color_hot = color_palette[1]
    random_goal_color_cold =  color_palette[4]
    random_goal_color_hot =  color_palette[5]

    flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
    color_palette = sns.color_palette(flatui)
    default_color = color_palette[4]

    path_in_order = []
    path_in_order.append(os.path.join(dataset_path, 'random_goal', '10', 'data.json'))
    path_in_order.append(os.path.join(dataset_path, 'random_goal', '11', 'data.json'))
    path_in_order.append(os.path.join(dataset_path, 'random_goal', '12', 'data.json'))
    path_in_order.append(os.path.join(dataset_path, 'random_params', '10', 'data.json'))
    path_in_order.append(os.path.join(dataset_path, 'random_params', '11', 'data.json'))
    path_in_order.append(os.path.join(dataset_path, 'random_params', '12', 'data.json'))

    data_in_order = []
    for data_file in path_in_order:
        data_in_order.append(load_dataset(data_file))

    colors_in_order = []
    colors_in_order.append(random_goal_color_hot)
    colors_in_order.append(random_goal_color_hot)
    colors_in_order.append(random_goal_color_hot)
    colors_in_order.append(random_params_color_hot)
    colors_in_order.append(random_params_color_hot)
    colors_in_order.append(random_params_color_hot)


    title_in_order = []
    title_in_order.append('CA - Run 1')
    title_in_order.append('CA - Run 2')
    title_in_order.append('CA - Run 3')
    title_in_order.append('Random - Run 1')
    title_in_order.append('Random - Run 2')
    title_in_order.append('Random - Run 3')

    # plt.ion()

    def plot_raw_exploration_no_temperature_control(ax, data, color='b'):

        x = np.array(data['features']['speed']) * 20.0
        y = data['features']['wobble']

        ax.scatter(x, y, 100, c=color)

        # ax.axis('scaled')

        ax.set_xlim([-1.5, 21.5])
        ax.set_ylim([-0.01, 0.6])
        ax.set_xlabel('Droplet Speed / $mm.s^{-1}$', fontsize=fontsize)
        ax.set_ylabel('Deformation in time / AU', fontsize=fontsize)

        plt.tight_layout()


    DPI=50
    STEPPING = 1000


    ## exploration
    # fig  = plt.figure(figsize=(2400/DPI,1800/DPI))
    # fig  = plt.figure(figsize=(1600/DPI,1200/DPI))
    # fig  = plt.figure(figsize=(1600/DPI,900/DPI))
    axs = []
    for i in range(6):
        fig  = plt.figure(figsize=(600/DPI,600/DPI))
        with sns.axes_style("ticks"):
            ax = plt.subplot(1,1,1)
            plot_raw_exploration_no_temperature_control(ax, data_in_order[i], color=colors_in_order[i])
            ax.set_title(title_in_order[i], fontsize=fontsize)
            plt.tight_layout()
            save_it(fig, plot_path, '{}'.format(title_in_order[i]), dpi=DPI)

            print '### {} ###'.format(title_in_order[i])
            print 'Start: {}'.format(data_in_order[i]['xp_info']['start_ctime'][0])
            print 'Start (10th): {}'.format(data_in_order[i]['xp_info']['start_ctime'][10])
            print 'End: {}'.format(data_in_order[i]['xp_info']['start_ctime'][-1])
