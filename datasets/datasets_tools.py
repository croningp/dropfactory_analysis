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


if __name__ == '__main__':

    data = load_dataset('random_params/110/data.json')

    import matplotlib
    import matplotlib.pyplot as plt

    plt.figure()
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['covered_arena_area']
    plt.scatter(x, y)

    # for k in data['droplet_features'].keys():
    #     plt.figure()
    #     y = data['droplet_features'][k]
    #     plt.scatter(x, y)
    #     plt.ylabel(k)

    plt.figure()
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['median_absolute_circularity_deviation']
    plt.scatter(x, y)

    plt.figure()
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['average_number_of_droplets']
    plt.scatter(x, y)

    plt.figure()
    x = data['droplet_features']['ratio_frame_active']
    y = data['droplet_features']['average_speed']
    plt.scatter(x, y)
    

    data = load_dataset('random_goal/110/data.json')

    import matplotlib
    import matplotlib.pyplot as plt

    plt.figure()
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['covered_arena_area']
    plt.scatter(x, y)

    plt.figure()
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['median_absolute_circularity_deviation']
    plt.scatter(x, y)

    plt.figure()
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['average_number_of_droplets']
    plt.scatter(x, y)

    plt.figure()
    x = data['droplet_features']['ratio_frame_active']
    y = data['droplet_features']['average_speed']
    plt.scatter(x, y)
