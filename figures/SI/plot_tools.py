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

from utils.plotting import plot_kde
from utils.exploration import compute_explored_volume
from utils.exploration import compute_volume_concave_hull


# design figure
fontsize = 34
matplotlib.rc('xtick', labelsize=30)
matplotlib.rc('ytick', labelsize=30)
matplotlib.rcParams.update({'font.size': fontsize})

X_FEATURE_NAME = 'average_speed'
Y_FEATURE_NAME = 'average_number_of_droplets'

X_FEATURE_LABEL = 'Droplet Speed / $mm.s^{-1}$'
Y_FEATURE_LABEL = 'No. of Droplets'

MIN_FEATURE_LIM = -1.5
MAX_FEATURE_LIM = 21.5

X_NORMALIZATION_RATIO = 1.0/20.0
Y_NORMALIZATION_RATIO = 1.0/20.0

ALPHA = 15
RADIUS_COVERAGE = 0.02

X_MARGIN_PLOT = 20
BIN_SIZE = 20

LINEWIDTH = 3


def plot_goals(ax, data, color='b'):

    goals = np.array(data['algorithm_info']['targeted_features'])
    x = goals[:, 0] / X_NORMALIZATION_RATIO
    y = goals[:, 1] / Y_NORMALIZATION_RATIO

    ax.scatter(x, y, 100, c=color)

    ax.axis('scaled')

    ax.set_xlim([MIN_FEATURE_LIM, MAX_FEATURE_LIM])
    ax.set_ylim([MIN_FEATURE_LIM, MAX_FEATURE_LIM])
    ax.set_xlabel(X_FEATURE_LABEL, fontsize=fontsize)
    ax.set_ylabel(Y_FEATURE_LABEL, fontsize=fontsize)

    ax.set_title('Goals', fontsize=fontsize)

    plt.tight_layout()



def plot_raw_exploration(ax, data, color='b'):

    x = data['droplet_features'][X_FEATURE_NAME]
    y = data['droplet_features'][Y_FEATURE_NAME]

    ax.scatter(x, y, 100, c=color)

    ax.axis('scaled')

    ax.set_xlim([MIN_FEATURE_LIM, MAX_FEATURE_LIM])
    ax.set_ylim([MIN_FEATURE_LIM, MAX_FEATURE_LIM])
    ax.set_xlabel(X_FEATURE_LABEL, fontsize=fontsize)
    ax.set_ylabel(Y_FEATURE_LABEL, fontsize=fontsize)

    ax.set_title('Observations', fontsize=fontsize)

    plt.tight_layout()


def plot_density(fig, ax, data, show_colorbar=True):

    x = data['droplet_features'][X_FEATURE_NAME]
    y = data['droplet_features'][Y_FEATURE_NAME]

    kde_data = np.array([x, y])
    cmap = plt.cm.jet
    cax = plot_kde(ax, kde_data, bounds = [MIN_FEATURE_LIM, MAX_FEATURE_LIM, MIN_FEATURE_LIM, MAX_FEATURE_LIM], bandwidth=0.3, cmap=cmap)

    if show_colorbar:
        cbar = fig.colorbar(cax, ax=ax)

    ax.axis('scaled')

    ax.set_xlim([MIN_FEATURE_LIM, MAX_FEATURE_LIM])
    ax.set_ylim([MIN_FEATURE_LIM, MAX_FEATURE_LIM])
    ax.set_xlabel(X_FEATURE_LABEL, fontsize=fontsize)
    ax.set_ylabel(Y_FEATURE_LABEL, fontsize=fontsize)

    ax.set_title('Observations Density', fontsize=fontsize)

    plt.tight_layout()

    return cax, cbar


def plot_coverage(ax, data, color='b'):

    x = np.array(data['droplet_features'][X_FEATURE_NAME]) * X_NORMALIZATION_RATIO
    y = np.array(data['droplet_features'][Y_FEATURE_NAME]) * Y_NORMALIZATION_RATIO

    X = np.array([x, y]).T
    # coverage = compute_explored_volume(X, RADIUS_COVERAGE)
    # ax.plot(coverage, color=color, linewidth=LINEWIDTH)

    volumes, concave_hull, edge_points = compute_volume_concave_hull(X, ALPHA)
    ax.plot(volumes, color=color, linewidth=LINEWIDTH)

    ax.set_xlim([-X_MARGIN_PLOT, 1000+X_MARGIN_PLOT])
    ax.set_ylim([0, 0.35])
    ax.set_xlabel('Iterations', fontsize=fontsize)
    ax.set_ylabel('Exploration Measure / $AU$', fontsize=fontsize)

    ax.set_title('Exploration', fontsize=fontsize)

    plt.tight_layout()


def clean_array(data_array):
    return data_array[np.logical_not(np.equal(data_array, None))]

def plot_temperature(ax, data, color='b', mean_line=True, print_title=True):

    temperature = np.array(data['xp_info']['temperature'])

    mean_temperature = round(np.mean(clean_array(temperature)), 2)
    std_temperature = round(np.std(clean_array(temperature)), 2)

    ax.plot(temperature, color=color, linewidth=LINEWIDTH)
    if mean_line:
        ax.plot([-X_MARGIN_PLOT, 1000+X_MARGIN_PLOT], [mean_temperature, mean_temperature], 'k--')

    ax.set_xlim([-X_MARGIN_PLOT, 1000+X_MARGIN_PLOT])
    ax.set_ylim([20, 30])
    ax.set_xlabel('Experiment Number', fontsize=fontsize)
    ax.set_ylabel('Temperature / ${^o}C$', fontsize=fontsize)

    if print_title:
        ax.set_title('T = {}$\pm${} {}'.format(mean_temperature, std_temperature, '${^o}C$'), fontsize=fontsize)

    plt.tight_layout()


def plot_humidity(ax, data, color='b', mean_line=True, print_title=True):

    humidity = np.array(data['xp_info']['humidity'])

    mean_humidity = round(np.mean(clean_array(humidity)), 2)
    std_humidity = round(np.std(clean_array(humidity)), 2)

    ax.plot(humidity, color=color, linewidth=LINEWIDTH)
    if mean_line:
        ax.plot([-X_MARGIN_PLOT, 1000+X_MARGIN_PLOT], [mean_humidity, mean_humidity], 'k--')

    ax.set_xlim([-X_MARGIN_PLOT, 1000+X_MARGIN_PLOT])
    ax.set_ylim([0, 100])
    ax.set_xlabel('Experiment Number', fontsize=fontsize)
    ax.set_ylabel('Humidity / %', fontsize=fontsize)

    if print_title:
        ax.set_title('H = {}$\pm${} {}'.format(mean_humidity, std_humidity, '%'), fontsize=fontsize)

    plt.tight_layout()


def plot_distribution_oil(ax, data, oil_name, normalized=False, color='b'):

    if normalized:
        oil_data = data['droplet_composition']['norm_json_form']
        str_xlabel = 'Ratio of \'{}\''.format(oil_name)
    else:
        oil_data = data['droplet_composition']['json_form']
        str_xlabel = 'Amount of \'{}\''.format(oil_name)

    values = []
    for oil_dict in oil_data:
        values.append(oil_dict[oil_name])

    bin_range = [0, 1]

    sns.distplot(values, bins=BIN_SIZE, hist_kws={'range': bin_range}, color=color, ax=ax)

    ax.set_xlim(bin_range)
    ax.set_xlabel(str_xlabel, fontsize=fontsize)
    ax.set_ylabel('Probability Density', fontsize=fontsize)

    plt.tight_layout()


def plot_distribution_properties(ax, data, property_name, color='b'):

    values = data['droplet_properties'][property_name]

    if property_name == 'viscosity':
        bin_range = [3, 11]
        property_label_name = 'Viscosity / $mPa.s$'

    if property_name == 'surface_tension':
        bin_range = [25, 32]
        property_label_name = 'Surface Tension / $mN.m^{-1}$'

    if property_name == 'density':
        bin_range = [0.8, 1.1]
        property_label_name = 'Density / $g.mL^{-1}$'

    sns.distplot(values, bins=BIN_SIZE, hist_kws={'range': bin_range}, color=color, ax=ax)

    ax.set_xlim(bin_range)
    ax.set_xlabel(property_label_name, fontsize=fontsize)
    ax.set_ylabel('Probability Density', fontsize=fontsize)

    plt.tight_layout()


def plot_distribution_features(ax, data, feature_name, color='b'):

    values = np.array(data['droplet_features'][feature_name])

    if feature_name == 'ratio_frame_active':
        bin_range = [0, 1]
        feature_name_name = '% Frame w. Droplets'

    if feature_name == 'average_speed':
        bin_range = [0, 20]
        feature_name_name = 'Droplet Speed / $mm.s^{-1}$'

    if feature_name == 'max_average_single_droplet_speed':
        bin_range = [0, 40]
        feature_name_name = 'Max Droplet Speed / $mm.s^{-1}$'

    if feature_name == 'average_number_of_droplets':
        bin_range = [0, 20]
        feature_name_name = 'No. of Droplets'

    if feature_name == 'average_number_of_droplets_last_second':
        bin_range = [0, 20]
        feature_name_name = 'No. Droplets Last Second'

    if feature_name == 'average_area':
        bin_range = [0, 30]
        feature_name_name = 'Droplets Area / $mm^2$'

    if feature_name == 'covered_arena_area':
        bin_range = [0, 1]
        feature_name_name = '% Area Covered'

    if feature_name == 'total_droplet_path_length':
        values = values / 1000.0 # in m
        bin_range = [0, 6]
        feature_name_name = 'Droplet Path Length / $m$'

    if feature_name == 'average_spread':
        bin_range = [0, 8]
        feature_name_name = 'Spread / $mm$'

    if feature_name == 'average_circularity':
        bin_range = [0.8, 1]
        feature_name_name = 'Circularity'

    if feature_name == 'median_absolute_circularity_deviation':
        bin_range = [0, 0.05]
        feature_name_name = 'Circularity Deviation'

    sns.distplot(values, bins=BIN_SIZE, hist_kws={'range': bin_range}, color=color, ax=ax)

    ax.set_xlim(bin_range)
    ax.set_xlabel(feature_name_name, fontsize=fontsize)
    ax.set_ylabel('Probability Density', fontsize=fontsize)

    plt.tight_layout()


def plot_exploration_platter(data, color='b'):

    N_ROW = 3
    N_COLUMN = 2

    fig  = plt.figure(figsize=(N_COLUMN*8,N_ROW*8))
    with sns.axes_style("ticks"):
        ax = plt.subplot(N_ROW,N_COLUMN,1)
        plot_raw_exploration(ax, data, color)

        ax = plt.subplot(N_ROW,N_COLUMN,2)
        plot_density(fig, ax, data, show_colorbar=True)

        ax = plt.subplot(N_ROW,N_COLUMN,3)
        plot_distribution_features(ax, data, 'average_speed', color=color)

        ax = plt.subplot(N_ROW,N_COLUMN,4)
        plot_distribution_features(ax, data, 'average_number_of_droplets', color=color)

        ax = plt.subplot(N_ROW,N_COLUMN,(5,6))
        plot_coverage(ax, data, color)

    return fig


def plot_oil_usage_platter(data, normalized=False, color='b'):

    N_ROW = 2
    N_COLUMN = 2

    fig  = plt.figure(figsize=(N_COLUMN*8,N_ROW*8))
    with sns.axes_style("ticks"):
        ax = plt.subplot(N_ROW,N_COLUMN,1)
        plot_distribution_oil(ax, data, oil_name='dep', normalized=normalized, color=color)

        ax = plt.subplot(N_ROW,N_COLUMN,2)
        plot_distribution_oil(ax, data, oil_name='octanol', normalized=normalized, color=color)

        ax = plt.subplot(N_ROW,N_COLUMN,3)
        plot_distribution_oil(ax, data, oil_name='pentanol', normalized=normalized, color=color)

        ax = plt.subplot(N_ROW,N_COLUMN,4)
        plot_distribution_oil(ax, data, oil_name='octanoic', normalized=normalized, color=color)

    return fig

def plot_info_platter(data, color='b'):

    N_ROW = 1
    N_COLUMN = 2

    fig  = plt.figure(figsize=(N_COLUMN*8,N_ROW*8))
    with sns.axes_style("ticks"):
        ax = plt.subplot(N_ROW,N_COLUMN,1)
        plot_temperature(ax, data, color=color)

        ax = plt.subplot(N_ROW,N_COLUMN,2)
        plot_humidity(ax, data, color=color)

    return fig


def plot_features_platter(data, color='b'):

    N_ROW = 4
    N_COLUMN = 3

    fig  = plt.figure(figsize=(N_COLUMN*8,N_ROW*8))
    with sns.axes_style("ticks"):
        for i, k in enumerate(data['droplet_features'].keys()):
            ax = plt.subplot(N_ROW,N_COLUMN,i+1)
            plot_distribution_features(ax, data, k, color=color)

    return fig


def plot_properties_platter(data, color='b'):

    N_ROW = 1
    N_COLUMN = 3

    fig  = plt.figure(figsize=(N_COLUMN*8,N_ROW*8))
    with sns.axes_style("ticks"):
        for i, k in enumerate(data['droplet_properties'].keys()):
            ax = plt.subplot(N_ROW,N_COLUMN,i+1)
            plot_distribution_properties(ax, data, k, color=color)

    return fig


if __name__ == '__main__':

    import filetools
    from utils.plotting import save_and_close_fig

    from datasets.datasets_tools import load_dataset
    from datasets.datasets_tools import forge_dataset_filename

    data = load_dataset(forge_dataset_filename('random_params', '111'))

    data = load_dataset(forge_dataset_filename('random_goal', '111_speed_division'))

    # fig  = plt.figure(figsize=(8,8))
    # with sns.axes_style("ticks"):
    #     ax = plt.subplot(111)

    # plot_goals(ax, data)
    # plot_raw_exploration(ax, data)
    # plot_density(ax, data)
    # plot_coverage(ax, data)
    # plot_temperature(ax, data)
    # plot_humidity(ax, data)
    # plot_distribution_oil(ax, data, oil_name='dep', normalized=True, color='b')
    # plot_distribution_properties(ax, data, 'viscosity', color='b')
    # plot_distribution_features(ax, data, 'average_speed', color='b')

    # fig = plot_exploration_platter(data)
    # fig = plot_oil_usage_platter(data, normalized=True)
    # fig = plot_info_platter(data)
    # fig = plot_features_platter(data)
    fig = plot_properties_platter(data)

    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    figure_filebasename = os.path.join(plot_folder, 'dev')
    save_and_close_fig(fig, figure_filebasename)
