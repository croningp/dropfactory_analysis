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
from datasets.datasets_tools import get_dataset_basepath


import filetools

import numpy as np

def sorted_path_by_speed(data):
    paths = np.array(data['paths'])
    speeds = np.array(data['droplet_features']['average_speed'])
    sorted_indices = np.argsort(speeds)
    return paths[sorted_indices], speeds[sorted_indices]

if __name__ == '__main__':

    from datasets.datasets_tools import save_list_to_csv


    dataset_path = get_dataset_basepath()
    csv_path = os.path.join(HERE_PATH, 'csv')

    targets_ranking = [-50, -10, -1]

    data_files = filetools.list_files(dataset_path, 'data.json')
    for data_file in data_files:
        print data_file
        data = load_dataset(data_file)
        sorted_paths, sorted_speeds = sorted_path_by_speed(data)

        data_list = []

        column_names = []
        column_names.append('ranking')
        column_names.append('speed')
        column_names.append('path')
        data_list.append(column_names)

        for target in targets_ranking:
            data_row = []
            data_row.append(target)
            data_row.append(sorted_speeds[target])
            data_row.append(sorted_paths[target])
            data_list.append(data_row)

        save_folder = os.path.split(data_file)[0].replace(dataset_path, csv_path)
        filetools.ensure_dir(save_folder)
        filename = os.path.join(save_folder, 'speed_sort.csv')
        save_list_to_csv(data_list, filename)
