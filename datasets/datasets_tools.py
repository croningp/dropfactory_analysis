import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import sys
root_path = os.path.join(HERE_PATH, '..')
sys.path.append(root_path)


from utils.tools import read_from_json


def format_data(raw_data):
    info = raw_data['info']
    experiments = raw_data['experiments']

    ##
    data = {}
    data['droplet_features'] = {}
    for k in experiments[0]['droplet_features'].keys():
        data['droplet_features'][k] = [xp['droplet_features'][k] for xp in raw_data['experiments']]

    return data


class LoadingError(Exception):
    pass


def load_dataset(dataset_filename):

    if not os.path.exists(dataset_filename):
        raise LoadingError('{} does not exist'.format(dataset_filename))

    return format_data(read_from_json(dataset_filename))


def forge_dataset_filename(method, seed):
    return os.path.join(HERE_PATH, method, seed, 'data.json')
