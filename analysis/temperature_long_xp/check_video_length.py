import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import filetools

from utils.plotting import save_and_close_fig
from utils.temperature_tools import load_recipes
from utils.tools import save_to_json
from utils.tools import read_from_json

DATA_PATH = os.path.join(HERE_PATH, 'extracted_data')

TIME_FEATURES_FILENAME = 'time_features.json'
PARAMS_FILENAME = 'params.json'
RUN_INFO_FILENAME=  'run_info.json'


if __name__ == '__main__':

    files = filetools.list_files(DATA_PATH, [TIME_FEATURES_FILENAME])

    lengths = []
    for j, filename in enumerate(files):
        result_folder = os.path.split(filename)[0]

        features_filename = os.path.join(result_folder, TIME_FEATURES_FILENAME)
        features = read_from_json(features_filename)

        lengths.append(len(features['average_speed']))

    # plt.scatter(range(len(files)), lengths)


    print np.array(files)[np.array(lengths) < 860]
