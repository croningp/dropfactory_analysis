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
from utils.exploration import compute_explored_volume


METHOD_NAMES = ['random_params', 'random_goal']
SEEDS = ['110', '111', '112', '210', '211', '212']
X_FEATURE_NAME = 'average_speed'
Y_FEATURE_NAME = 'average_number_of_droplets'
X_NORMALIZATION_RATIO = 1.0/20.0
Y_NORMALIZATION_RATIO = 1.0/20.0

RADIUS = 0.02

if __name__ == '__main__':

    N_METHODS = len(METHOD_NAMES)
    N_SEEDS = len(SEEDS)

    coverage_data = {}

    for i_method_name, method_name in enumerate(METHOD_NAMES):
        all_method_coverages = []
        coverage_data[method_name] = {}
        for i_seed, seed in enumerate(SEEDS):

            if method_name != 'random_params':
                seed_name = '{}_speed_division'.format(seed)
            else:
                seed_name = seed
            data = load_dataset(forge_dataset_filename(method_name, seed_name))
            x = np.array(data['droplet_features'][X_FEATURE_NAME]) * X_NORMALIZATION_RATIO
            y = np.array(data['droplet_features'][Y_FEATURE_NAME]) * Y_NORMALIZATION_RATIO

            X = np.array([x, y]).T
            coverage = compute_explored_volume(X, RADIUS)

            ##
            coverage_data[method_name][seed] = coverage
            #
            all_method_coverages.append(coverage)

    ##
    import filetools
    from utils.tools import save_to_json

    data_folder = os.path.join(HERE_PATH, 'data')
    filetools.ensure_dir(data_folder)

    savefilename = os.path.join(data_folder, 'coverages.json')
    save_to_json(coverage_data, savefilename)
