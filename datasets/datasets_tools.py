import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import sys
root_path = os.path.join(HERE_PATH, '..')
sys.path.append(root_path)

from constants import DATASET_FILENAME
from constants import REPEATS_FILENAME
from utils.tools import read_from_json

class LoadingError(Exception):
    pass


def format_data(raw_data):
    info = raw_data['info']
    experiments = raw_data['experiments']

    ##
    data = {}
    data['droplet_features'] = {}
    for k in experiments[0]['droplet_features'].keys():
        data['droplet_features'][k] = [xp['droplet_features'][k] for xp in raw_data['experiments']]

    return data


def load_dataset(dataset_filename):

    if not os.path.exists(dataset_filename):
        raise LoadingError('{} does not exist'.format(dataset_filename))

    return format_data(read_from_json(dataset_filename))


def forge_dataset_filename(method, seed):
    return os.path.join(HERE_PATH, method, seed, DATASET_FILENAME)

##
def format_repeats(raw_data):
    info = raw_data['info']
    experiments = raw_data['experiments']

    ##
    repeats = []
    for i_xp in range(len(experiments)):
        data = {}
        data['xp_number'] = info['xp_number'][i_xp]

        data['droplet_features'] = {}
        for k in experiments[i_xp]['original']['droplet_features'].keys():
            data['droplet_features'][k] = []
            # the first is the original
            # data['droplet_features'][k].append(experiments[i_xp]['original']['droplet_features'][k])
            # the remainings are repeats
            for i_repeat in range(len(experiments[i_xp]['repeats'])):
                data['droplet_features'][k].append(experiments[i_xp]['repeats'][i_repeat]['droplet_features'][k])

        repeats.append(data)

    return repeats


def load_repeats(dataset_filename):

    if not os.path.exists(dataset_filename):
        raise LoadingError('{} does not exist'.format(dataset_filename))

    return format_repeats(read_from_json(dataset_filename))


def forge_repeats_filename(method, seed):
    return os.path.join(HERE_PATH, method, seed, REPEATS_FILENAME)
