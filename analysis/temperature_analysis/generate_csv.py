import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

from utils.temperature_tools import load_temperature_dataset
from utils.temperature_tools import load_recipes
from utils.temperature_tools import find_row

import filetools

#
import csv

def save_list_to_csv(data_list, filename):
    with open(filename, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ')
        for data in data_list:
            csvwriter.writerow(data)


def build_csv(datasets, filename):

    data_list = []

    ##
    column_names = []
    column_names.append('path')
    column_names.extend(["dep", "octanol", "octanoic", "pentanol"])
    column_names.append('temperature')
    column_names.append('humidity')
    for k, v in datasets['droplet_features'].items():
        column_names.append(k)
    for k, v in datasets['droplet_properties'].items():
        column_names.append(k)

    data_list.append(column_names)

    ##
    for i in range(len(datasets['paths'])):
        data_row = []
        data_row.append(datasets['paths'][i])
        data_row.extend(datasets['droplet_composition']['ratio_vector_form'][i])
        data_row.append(datasets['xp_info']['temperature'][i])
        data_row.append(datasets['xp_info']['humidity'][i])
        for k, v in datasets['droplet_features'].items():
            data_row.append(v[i])
        for k, v in datasets['droplet_properties'].items():
            data_row.append(v[i])

        data_list.append(data_row)

    ##
    save_list_to_csv(data_list, filename)


if __name__ == '__main__':


    dataset = load_temperature_dataset()

    save_dir = os.path.join(HERE_PATH, 'csv')
    filetools.ensure_dir(save_dir)

    #
    import numpy as np
    from datasets.datasets_tools import sub_dataset

    X = np.array(dataset['droplet_composition']['vector_form'])
    recipes = load_recipes()

    for i in range(recipes.shape[0]):
        index = find_row(X, recipes[i,:])

        sub_data = sub_dataset(dataset, index)

        filename =  os.path.join(save_dir, '{}.csv'.format(i))
        build_csv(sub_data, filename)
