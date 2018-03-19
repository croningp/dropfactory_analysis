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

import numpy as np

from utils.exploration import compute_volume_convex_hull
from utils.exploration import compute_volume_concave_hull

import matplotlib.pyplot as plt
from utils.plotting import plot_convex_hull
from utils.plotting import plot_concave_hull
from utils.plotting import save_and_close_fig


METHOD_NAMES = ['random_params', 'random_goal']
SEEDS = ['110', '111', '112']
X_FEATURE_NAME = 'average_speed'
Y_FEATURE_NAME = 'average_number_of_droplets'
X_NORMALIZATION_RATIO = 1.0/20.0
Y_NORMALIZATION_RATIO = 1.0/20.0

ALPHA = 15

if __name__ == '__main__':

    import filetools

    plot_folder = os.path.join(HERE_PATH, 'plot_hull')
    filetools.ensure_dir(plot_folder)

    N_METHODS = len(METHOD_NAMES)
    N_SEEDS = len(SEEDS)

    ## compute reference coverages
    X = None
    for i_method_name, method_name in enumerate(METHOD_NAMES):
        for i_seed, seed in enumerate(SEEDS):

            if method_name != 'random_params':
                seed_name = '{}_speed_division'.format(seed)
            else:
                seed_name = seed
            data = load_dataset(forge_dataset_filename(method_name, seed_name))
            x = np.array(data['droplet_features'][X_FEATURE_NAME]) * X_NORMALIZATION_RATIO
            y = np.array(data['droplet_features'][Y_FEATURE_NAME]) * Y_NORMALIZATION_RATIO

            data_points = np.array([x, y]).T

            if X is None:
                X = data_points
            else:
                X = np.vstack((X, data_points))

    global_volume_convex_hull, hull = compute_volume_convex_hull(X, last_only=True)
    global_volume_concave_hull, concave_hull, edge_points = compute_volume_concave_hull(X, ALPHA, last_only=True)

    fig = plt.figure(figsize=(10,8))
    plot_convex_hull(hull)
    plot_concave_hull(concave_hull, edge_points, X)
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    filebasename = os.path.join(plot_folder, 'global')
    save_and_close_fig(fig, filebasename)

    ###
    convex_hull_data = {}
    concave_hull_data = {}

    convex_hull_data['global_coverage'] = global_volume_convex_hull
    concave_hull_data['global_coverage'] = global_volume_concave_hull


    for i_method_name, method_name in enumerate(METHOD_NAMES):
        convex_hull_data[method_name] = {}
        concave_hull_data[method_name] = {}
        for i_seed, seed in enumerate(SEEDS):

            print('## {} {}'.format(method_name, seed))

            if method_name != 'random_params':
                seed_name = '{}_speed_division'.format(seed)
            else:
                seed_name = seed
            data = load_dataset(forge_dataset_filename(method_name, seed_name))
            x = np.array(data['droplet_features'][X_FEATURE_NAME]) * X_NORMALIZATION_RATIO
            y = np.array(data['droplet_features'][Y_FEATURE_NAME]) * Y_NORMALIZATION_RATIO

            X = np.array([x, y]).T
            volumes, hull = compute_volume_convex_hull(X)
            convex_hull_data[method_name][seed] = volumes

            ##
            volumes, concave_hull, edge_points = compute_volume_concave_hull(X, ALPHA)
            concave_hull_data[method_name][seed] = volumes

            fig = plt.figure(figsize=(10,8))
            plot_convex_hull(hull)
            plot_concave_hull(concave_hull, edge_points, X)
            plt.xlim([0, 1])
            plt.ylim([0, 1])
            filebasename = os.path.join(plot_folder, '{} {}'.format(method_name, seed))
            save_and_close_fig(fig, filebasename)

    ##
    from utils.tools import save_to_json

    data_folder = os.path.join(HERE_PATH, 'data')
    filetools.ensure_dir(data_folder)

    savefilename = os.path.join(data_folder, 'convex_hulls.json')
    save_to_json(convex_hull_data, savefilename)

    savefilename = os.path.join(data_folder, 'concave_hulls.json')
    save_to_json(concave_hull_data, savefilename)
