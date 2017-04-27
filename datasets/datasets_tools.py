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

    import matplotlib
    import matplotlib.pyplot as plt



    plt.figure(figsize=(16,8))

    data = load_dataset('random_params/110/data.json')
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['median_absolute_circularity_deviation']
    plt.subplot(1,2,1)
    plt.scatter(x, y, 50)
    plt.xlim([-1, 21])
    plt.ylim([-0.01, 0.21])
    plt.xlabel('Speed')
    plt.ylabel('Deformation')

    data = load_dataset('random_goal/110_speed_deformation/data.json')
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['median_absolute_circularity_deviation']
    plt.subplot(1,2,2)
    plt.scatter(x, y, 50, 'r')
    plt.xlim([-1, 21])
    plt.ylim([-0.01, 0.21])
    plt.xlabel('Speed')
    plt.ylabel('Deformation')


    plt.figure(figsize=(16,8))

    data = load_dataset('random_params/110/data.json')
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['average_number_of_droplets']
    plt.subplot(1,2,1)
    plt.scatter(x, y, 50)
    plt.xlim([-1, 21])
    plt.ylim([-1, 21])
    plt.xlabel('Speed')
    plt.ylabel('Division')

    data = load_dataset('random_goal/110_speed_division/data.json')
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['average_number_of_droplets']
    plt.subplot(1,2,2)
    plt.scatter(x, y, 50, 'r')
    plt.xlim([-1, 21])
    plt.ylim([-1, 21])
    plt.xlabel('Speed')
    plt.ylabel('Division')


    #####

    plt.figure(figsize=(24,8))

    data = load_dataset('random_params/111/data.json')
    x = data['droplet_features']['covered_arena_area']
    y = data['droplet_features']['median_absolute_circularity_deviation']
    plt.subplot(1,3,1)
    plt.scatter(x, y, 50)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.01, 0.21])
    plt.xlabel('Coverage')
    plt.ylabel('Deformation')

    data = load_dataset('random_goal/110_speed_deformation/data.json')
    x = data['droplet_features']['covered_arena_area']
    y = data['droplet_features']['median_absolute_circularity_deviation']
    plt.subplot(1,3,2)
    plt.scatter(x, y, 50, 'r')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.01, 0.21])
    plt.xlabel('Coverage')
    plt.ylabel('Deformation')

    data = load_dataset('random_goal/110_speed_division/data.json')
    x = data['droplet_features']['covered_arena_area']
    y = data['droplet_features']['median_absolute_circularity_deviation']
    plt.subplot(1,3,3)
    plt.scatter(x, y, 50, 'r')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.01, 0.21])
    plt.xlabel('Coverage')
    plt.ylabel('Deformation')

    ##
    plt.figure(figsize=(16,8))

    data = load_dataset('random_params/112/data.json')
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['average_number_of_droplets']
    plt.subplot(1,2,1)
    plt.scatter(x, y, 50)
    plt.xlim([-1, 21])
    plt.ylim([-1, 21])
    plt.xlabel('Speed')
    plt.ylabel('Division')

    data = load_dataset('random_goal/112_speed_division/data.json')
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['average_number_of_droplets']
    plt.subplot(1,2,2)
    plt.scatter(x, y, 50, 'r')
    plt.xlim([-1, 21])
    plt.ylim([-1, 21])
    plt.xlabel('Speed')
    plt.ylabel('Division')

    ##

    plt.figure(figsize=(24,8))

    data = load_dataset('random_params/111/data.json')
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['average_number_of_droplets']
    plt.subplot(1,3,1)
    plt.scatter(x, y, 50)
    plt.xlim([-1, 21])
    plt.ylim([-1, 21])
    plt.xlabel('Speed')
    plt.ylabel('Division')

    data = load_dataset('random_goal/111_speed_division/data.json')
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['average_number_of_droplets']
    plt.subplot(1,3,2)
    plt.scatter(x, y, 50, 'r')
    plt.xlim([-1, 21])
    plt.ylim([-1, 21])
    plt.xlabel('Speed')
    plt.ylabel('Division')

    data = load_dataset('grid_search/5/data.json')
    x = data['droplet_features']['average_speed']
    y = data['droplet_features']['average_number_of_droplets']
    plt.subplot(1,3,3)
    plt.scatter(x, y, 50)
    plt.xlim([-1, 21])
    plt.ylim([-1, 21])
    plt.xlabel('Speed')
    plt.ylabel('Division')
