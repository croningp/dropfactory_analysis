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

from utils.plotting import save_and_close_fig

import plot_tools

def init_single_fig_ax():
    fig  = plt.figure(figsize=(8,8))
    with sns.axes_style("ticks"):
        ax = plt.subplot(111)
    return fig, ax

def save_it(fig, plot_folder, filebasename):

    for ext in ['.png', '.eps', '.svg']:
        plot_dir = os.path.join(plot_folder, ext[1:])
        filetools.ensure_dir(plot_dir)

        figure_filebasename = os.path.join(plot_dir, filebasename)

        save_and_close_fig(fig, figure_filebasename, exts=[ext])


def plot_it_all(data, plot_folder, color='b'):

    ## exploration
    fig, ax = init_single_fig_ax()
    plot_tools.plot_raw_exploration(ax, data, color=color)
    save_it(fig, plot_folder, 'exploration_raw')

    fig, ax = init_single_fig_ax()
    plot_tools.plot_density(ax, data, show_colorbar=True)
    save_it(fig, plot_folder, 'exploration_density')

    fig, ax = init_single_fig_ax()
    plot_tools.plot_coverage(ax, data, color=color)
    save_it(fig, plot_folder, 'exploration_coverage')

    fig = plot_tools.plot_exploration_platter(data, color=color)
    save_it(fig, plot_folder, 'exploration_platter')

    ## oil usage
    oil_names = data['droplet_composition']['json_form'][0].keys()

    for oil_name in oil_names:

        fig, ax = init_single_fig_ax()
        plot_tools.plot_distribution_oil(ax, data, oil_name=oil_name, normalized=False, color=color)
        save_name = 'oil_{}'.format(oil_name)
        save_it(fig, plot_folder, save_name)

        fig, ax = init_single_fig_ax()
        plot_tools.plot_distribution_oil(ax, data, oil_name=oil_name, normalized=True, color=color)
        save_name = 'oil_{}_normalized'.format(oil_name)
        save_it(fig, plot_folder, save_name)

    fig = plot_tools.plot_oil_usage_platter(data, normalized=False, color=color)
    save_it(fig, plot_folder, 'oil_platter')

    fig = plot_tools.plot_oil_usage_platter(data, normalized=True, color=color)
    save_it(fig, plot_folder, 'oil_platter_normalized')

    ## oil_properties
    properties_names = data['droplet_properties'].keys()
    for property_name in properties_names:
        fig, ax = init_single_fig_ax()
        plot_tools.plot_distribution_properties(ax, data, property_name=property_name, color=color)
        save_name = 'property_{}'.format(property_name)
        save_it(fig, plot_folder, save_name)

    fig = plot_tools.plot_properties_platter(data, color=color)
    save_it(fig, plot_folder, 'property_platter')

    ## droplet motion features
    feature_names = data['droplet_features'].keys()
    for feature_name in feature_names:
        fig, ax = init_single_fig_ax()
        plot_tools.plot_distribution_features(ax, data, feature_name=feature_name, color=color)
        save_name = 'feature_{}'.format(feature_name)
        save_it(fig, plot_folder, save_name)

    fig = plot_tools.plot_features_platter(data, color=color)
    save_it(fig, plot_folder, 'feature_platter')

    ## experiment info
    fig, ax = init_single_fig_ax()
    plot_tools.plot_temperature(ax, data, color=color)
    save_it(fig, plot_folder, 'info_temperature')

    fig, ax = init_single_fig_ax()
    plot_tools.plot_humidity(ax, data, color=color)
    save_it(fig, plot_folder, 'info_humidity')

    fig = plot_tools.plot_info_platter(data, color=color)
    save_it(fig, plot_folder, 'info_platter')


if __name__ == '__main__':

    import filetools

    from datasets.datasets_tools import load_dataset
    from datasets.datasets_tools import forge_dataset_filename
    from datasets.datasets_tools import get_dataset_basepath

    dataset_path = get_dataset_basepath()
    plot_path = os.path.join(HERE_PATH, 'plot')

    color_palette = sns.color_palette("Paired")
    random_params_color = color_palette[1]
    random_goal_color =  color_palette[5]

    flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
    color_palette = sns.color_palette(flatui)
    default_color = color_palette[4]

    data_files = filetools.list_files(dataset_path, 'data.json')
    for data_file in data_files:
        data = load_dataset(data_file)
        if len(data['paths']) == 1000:
            plot_folder = os.path.split(data_file)[0].replace(dataset_path, plot_path)

            if 'random_goal' in plot_folder:
                color = random_goal_color
            elif 'random_params' in plot_folder:
                color = random_params_color
            else:
                color = default_color

            plot_it_all(data, plot_folder, color)
