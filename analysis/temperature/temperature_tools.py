import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

import numpy as np

from datasets.datasets_tools import load_dataset
from datasets.datasets_tools import forge_dataset_filename_from_path
from datasets.datasets_tools import join_datasets
from datasets.datasets_tools import get_dataset_basepath

import filetools

RECIPES_CSV_FILENAME = os.path.join(HERE_PATH, 'recipes_for_temperature_analysis.csv')
EXPERIMENT_FOLDER = os.path.join(HERE_PATH, 'experiments')

TEMPERATURE_DATA_RELPATH = 'manual_exploration/temperature_analysis/experiments'

def load_temperature_dataset():

    temperature_folders = filetools.list_folders(os.path.join(get_dataset_basepath(), TEMPERATURE_DATA_RELPATH))

    datasets = []
    for path in temperature_folders:
        datasets.append(load_dataset(forge_dataset_filename_from_path(path)))

    return join_datasets(*datasets)


def load_recipes():
    data = np.loadtxt(RECIPES_CSV_FILENAME, delimiter=',', skiprows=1)
    # order is dep,octanol,octanoic,pentanol
    return data

def unique_row(data):
    data = np.array(data)
    data_coded_by_row = np.ascontiguousarray(data).view(np.dtype((np.void, data.dtype.itemsize * data.shape[1])))
    _, idx = np.unique(data_coded_by_row, return_index=True)
    unique_data = data[idx]
    return unique_data

def find_row(X, row):
    return np.where((X == row).all(axis=1))[0]
