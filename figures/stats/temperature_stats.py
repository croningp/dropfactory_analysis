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

if __name__ == '__main__':

    METHOD_NAMES = ['random_params', 'random_goal']
    SEEDS = ['110', '111', '112', '210', '211', '212']


    N_METHODS = len(METHOD_NAMES)
    N_SEEDS = len(SEEDS)

    ## compute indivdual coverage
    temp_data = {}

    for i_method_name, method_name in enumerate(METHOD_NAMES):
        all_method_temp_data = []
        temp_data[method_name] = {}
        for i_seed, seed in enumerate(SEEDS):

            if method_name != 'random_params':
                seed_name = '{}_speed_division'.format(seed)
            else:
                seed_name = seed
            data = load_dataset(forge_dataset_filename(method_name, seed_name))

            temperature = np.array(data['xp_info']['temperature'])

            temp_data[method_name][seed] = temperature

    def clean_array(data_array):
        return data_array[np.logical_not(np.equal(data_array, None))]

    hot_temp = []
    hot_temp.extend(temp_data['random_params']['110'])
    hot_temp.extend(temp_data['random_params']['111'])
    hot_temp.extend(temp_data['random_params']['112'])
    hot_temp.extend(temp_data['random_goal']['110'])
    hot_temp.extend(temp_data['random_goal']['111'])
    hot_temp.extend(temp_data['random_goal']['112'])

    hot_temp = clean_array(np.array(hot_temp))
    print('Hot temperature: mean {} / std {}'.format(np.mean(hot_temp), np.std(hot_temp)))

    cold_temp = []
    cold_temp.extend(temp_data['random_params']['210'])
    cold_temp.extend(temp_data['random_params']['211'])
    cold_temp.extend(temp_data['random_params']['212'])
    cold_temp.extend(temp_data['random_goal']['210'])
    cold_temp.extend(temp_data['random_goal']['211'])
    cold_temp.extend(temp_data['random_goal']['212'])

    cold_temp = clean_array(np.array(cold_temp))
    print('Cold temperature: mean {} / std {}'.format(np.mean(cold_temp), np.std(cold_temp)))
