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
    fig  = plt.figure(figsize=(10,8))
    with sns.axes_style("ticks"):
        ax = plt.subplot(111)
    return fig, ax

def init_side_fig_ax():
    fig  = plt.figure(figsize=(16,8))
    with sns.axes_style("ticks"):
        ax1 = plt.subplot(121)
        ax2 = plt.subplot(122)
    return fig, ax1, ax2

def save_it(fig, plot_folder, filebasename, legend=None):

    for ext in ['.png', '.eps', '.svg']:
        plot_dir = os.path.join(plot_folder, ext[1:])
        filetools.ensure_dir(plot_dir)

        figure_filebasename = os.path.join(plot_dir, filebasename)

        save_and_close_fig(fig, figure_filebasename, exts=[ext], legend=legend)

###
###
###

color_palette = sns.color_palette("Paired")
random_params_color_cold = color_palette[0]
random_params_color_hot = color_palette[1]
random_goal_color_cold =  color_palette[4]
random_goal_color_hot =  color_palette[5]

flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
color_palette = sns.color_palette(flatui)
default_color = color_palette[4]


def color_from_path(path):
    if 'random_goal' in path:
        if '/1' in path:
            color = random_goal_color_hot
        else:
            color = random_goal_color_cold
    elif 'random_params' in path:
        if '/1' in path:
            color = random_params_color_hot
        else:
            color = random_params_color_cold
    else:
        color = default_color

    return color

def clean_array(data_array):
    return data_array[np.logical_not(np.equal(data_array, None))]


def title_from_path_and_data(path, data):
    if 'random_goal' in path:
        method_str = 'CA'
    elif 'random_params' in path:
        method_str = 'Random'
    else:
        method_str = os.path.split(path)[0].split('/')[-2]

    temperature = np.array(data['xp_info']['temperature'])
    mean_temperature = round(np.mean(clean_array(temperature)), 2)
    std_temperature = round(np.std(clean_array(temperature)), 2)
    temp_str = 'T = {}$\pm${} {}'.format(mean_temperature, std_temperature, '${^o}C$')

    seed_str = os.path.split(path)[0].split('/')[-1][0:3]

    return '{} \n {} \n Seed {}'.format(method_str, temp_str, seed_str)


def prepare_dict_kws(dataset_filename_left, dataset_filename_right):

    data_left = load_dataset(dataset_filename_left)
    data_right = load_dataset(dataset_filename_right)

    color_left = color_from_path(dataset_filename_left)
    color_right = color_from_path(dataset_filename_right)

    title_left = title_from_path_and_data(dataset_filename_left, data_left)
    title_right = title_from_path_and_data(dataset_filename_right, data_right)

    dict_kws = {
        'data_left': data_left,
        'color_left': color_left,
        'title_left': title_left,
        'data_right': data_right,
        'color_right': color_right,
        'title_right': title_right
    }

    return dict_kws

def plot_side_exploration(plot_folder, data_left, data_right, color_left, color_right, title_left, title_right):

    fig, ax1, ax2 = init_side_fig_ax()
    plot_tools.plot_raw_exploration(ax1, data_left, color=color_left)
    ax1.set_title(title_left, fontsize=fontsize)

    plot_tools.plot_raw_exploration(ax2, data_right, color=color_right)
    ax2.set_title(title_right, fontsize=fontsize)

    save_it(fig, plot_folder, 'exploration_raw')

def plot_side_density(plot_folder, data_left, data_right, color_left, color_right, title_left, title_right):

    fig, ax1, ax2 = init_side_fig_ax()
    plot_tools.plot_density(fig, ax1, data_left, show_colorbar=True)
    ax1.set_title(title_left, fontsize=fontsize)

    plot_tools.plot_density(fig, ax2, data_right, show_colorbar=True)
    ax2.set_title(title_right, fontsize=fontsize)

    save_it(fig, plot_folder, 'exploration_density')

def plot_side_density_same_scale(plot_folder, data_left, data_right, color_left, color_right, title_left, title_right):

    fig, ax1, ax2 = init_side_fig_ax()

    cax1, cbar1 = plot_tools.plot_density(fig, ax1, data_left, show_colorbar=True)
    ax1.set_title(title_left, fontsize=fontsize)

    cax2, cbar2 = plot_tools.plot_density(fig, ax2, data_right, show_colorbar=True)
    ax2.set_title(title_right, fontsize=fontsize)

    clim1 = cbar1.get_clim()
    clim2 = cbar2.get_clim()

    ticks1 = [float(t.get_text()) for t in cbar1.ax.get_yticklabels()]
    ticks2 = [float(t.get_text()) for t in cbar2.ax.get_yticklabels()]

    if ticks1[-1] < ticks2[-1]:
        cbar_ticks = ticks1
    else:
        cbar_ticks = ticks2

    min_clim = min(clim1[0], clim2[0])
    max_clim = min(clim1[1], clim2[1])
    clim = (min_clim, max_clim)
    cbar1.set_clim(clim)
    cbar1.set_ticks(cbar_ticks)
    cbar1.draw_all()

    cbar2.set_clim(clim)
    cbar2.set_ticks(cbar_ticks)
    cbar2.draw_all()

    plt.tight_layout()

    save_it(fig, plot_folder, 'exploration_density_same_scale')

def plot_side_coverage(plot_folder, data_left, data_right, color_left, color_right, title_left, title_right):

    fig, ax = init_single_fig_ax()
    plot_tools.plot_coverage(ax, data_left, color=color_left)
    plot_tools.plot_coverage(ax, data_right, color=color_right)
    legend = plt.legend([title_left, title_right], fontsize=fontsize, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.tight_layout()

    save_it(fig, plot_folder, 'exploration_coverage', legend=legend)


def plot_side_oil(plot_folder, oil_name, normalized, data_left, data_right, color_left, color_right, title_left, title_right):

    fig, ax = init_single_fig_ax()
    plot_tools.plot_distribution_oil(ax, data_left, oil_name=oil_name, normalized=normalized, color=color_left)
    plot_tools.plot_distribution_oil(ax, data_right, oil_name=oil_name, normalized=normalized, color=color_right)
    legend = plt.legend([title_left, title_right], fontsize=fontsize, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.tight_layout()

    if normalized:
        fname = 'oil_{}_normalized'.format(oil_name)
    else:
        fname = 'oil_{}'.format(oil_name)
    save_it(fig, plot_folder, fname, legend=legend)


def plot_side_property(plot_folder, property_name, data_left, data_right, color_left, color_right, title_left, title_right):

    fig, ax = init_single_fig_ax()
    plot_tools.plot_distribution_properties(ax, data_left, property_name=property_name, color=color_left)
    plot_tools.plot_distribution_properties(ax, data_right, property_name=property_name, color=color_right)
    legend = plt.legend([title_left, title_right], fontsize=fontsize, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.tight_layout()

    fname = 'property_{}'.format(property_name)
    save_it(fig, plot_folder, fname, legend=legend)

def plot_side_features(plot_folder, feature_name, data_left, data_right, color_left, color_right, title_left, title_right):

    fig, ax = init_single_fig_ax()
    plot_tools.plot_distribution_features(ax, data_left, feature_name=feature_name, color=color_left)
    plot_tools.plot_distribution_features(ax, data_right, feature_name=feature_name, color=color_right)
    legend = plt.legend([title_left, title_right], fontsize=fontsize, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.tight_layout()

    fname = 'feature_{}'.format(feature_name)
    save_it(fig, plot_folder, fname, legend=legend)


def plot_side_temperature(plot_folder, data_left, data_right, color_left, color_right, title_left, title_right):

    fig, ax = init_single_fig_ax()
    plot_tools.plot_temperature(ax, data_left, color=color_left, mean_line=False, print_title=False)
    plot_tools.plot_temperature(ax, data_right, color=color_right, mean_line=False, print_title=False)
    legend = plt.legend([title_left, title_right], fontsize=fontsize, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.tight_layout()

    save_it(fig, plot_folder, 'info_temperature', legend=legend)


def plot_side_humidity(plot_folder, data_left, data_right, color_left, color_right, title_left, title_right):

    fig, ax = init_single_fig_ax()
    plot_tools.plot_humidity(ax, data_left, color=color_left, mean_line=False, print_title=False)
    plot_tools.plot_humidity(ax, data_right, color=color_right, mean_line=False, print_title=False)
    legend = plt.legend([title_left, title_right], fontsize=fontsize, bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.tight_layout()

    save_it(fig, plot_folder, 'info_humidity', legend=legend)


def plot_all_side(plot_path, **dict_kws):
    data_sample = dict_kws['data_left']
    oil_names = data_sample['droplet_composition']['json_form'][0].keys()
    properties_names = data_sample['droplet_properties'].keys()
    feature_names = data_sample['droplet_features'].keys()

    plot_side_exploration(plot_path, **dict_kws)
    plot_side_density(plot_path, **dict_kws)
    plot_side_density_same_scale(plot_path, **dict_kws)
    plot_side_coverage(plot_path, **dict_kws)

    for oil_name in oil_names:
        for normalized in [True, False]:
            plot_side_oil(plot_path, oil_name, normalized=normalized, **dict_kws)
            plot_side_oil(plot_path, oil_name, normalized=normalized, **dict_kws)

    for property_name in properties_names:
        plot_side_property(plot_path, property_name, **dict_kws)

    for feature_name in feature_names:
        plot_side_features(plot_path, feature_name, **dict_kws)

    plot_side_temperature(plot_path, **dict_kws)
    plot_side_humidity(plot_path, **dict_kws)

if __name__ == '__main__':

    import filetools

    from datasets.datasets_tools import load_dataset
    from datasets.datasets_tools import forge_dataset_filename
    from datasets.datasets_tools import get_dataset_basepath

    dataset_path = get_dataset_basepath()
    root_plot_path = os.path.join(HERE_PATH, 'plot', 'side_by_side')

    for seed in ['110', '111', '112', '210', '211', '212']:
        plot_path = os.path.join(root_plot_path, 'params_vs_goal', seed)
        print plot_path

        dataset_filename_left = forge_dataset_filename('random_params', seed)
        dataset_filename_right = forge_dataset_filename('random_goal', '{}_speed_division'.format(seed))

        dict_kws = prepare_dict_kws(dataset_filename_left, dataset_filename_right)

        plot_all_side(plot_path, **dict_kws)

    for method in ['random_params', 'random_goal']:
        for seed_ext in ['0', '1', '2']:
            plot_path = os.path.join(root_plot_path, 'cold_vs_hot', '{}_{}'.format(method, seed_ext))
            print plot_path

            if method == 'random_goal':
                dataset_filename_left = forge_dataset_filename(method, '21{}_speed_division'.format(seed_ext))
                dataset_filename_right = forge_dataset_filename(method, '11{}_speed_division'.format(seed_ext))
            else:
                dataset_filename_left = forge_dataset_filename(method, '21{}'.format(seed_ext))
                dataset_filename_right = forge_dataset_filename(method, '11{}'.format(seed_ext))

            dict_kws = prepare_dict_kws(dataset_filename_left, dataset_filename_right)

            plot_all_side(plot_path, **dict_kws)
