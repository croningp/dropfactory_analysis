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

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})

PLOT_FOLDER = os.path.join(HERE_PATH, 'plots')
filetools.ensure_dir(PLOT_FOLDER)

DATA_PATH = os.path.join(HERE_PATH, 'extracted_data')

TIME_FEATURES_FILENAME = 'time_features.json'
PARAMS_FILENAME = 'params.json'
RUN_INFO_FILENAME=  'run_info.json'


def plot_xp(save_folder, features, params, run_info):
    filetools.ensure_dir(save_folder)

    for k, v in features.items():
        y = features[k]
        x = range(len(y))

        fig = plt.figure(figsize=(12,8))
        plt.scatter(x, y, 50, 'b')
        plt.xlabel('Time (s)', fontsize=fontsize)
        plt.ylabel(k, fontsize=fontsize)

        normalized_recipy = params['oil_formulation']
        total = np.sum(normalized_recipy.values())
        for key, value in normalized_recipy.items():
            normalized_recipy[key] = np.round(100*(value / total))

        title = '{} | Temperature = {}'.format(normalized_recipy, run_info['temperature'])
        plt.title(title)
        plt.tight_layout()

        plotfilebasename = os.path.join(save_folder, k)
        save_and_close_fig(fig, plotfilebasename, exts=['.png'])


if __name__ == '__main__':

    files = filetools.list_files(DATA_PATH, [TIME_FEATURES_FILENAME])
    recipes = load_recipes()


    for j, filename in enumerate(files):
        result_folder = os.path.split(filename)[0]

        features_filename = os.path.join(result_folder, TIME_FEATURES_FILENAME)
        params_filename = os.path.join(result_folder, PARAMS_FILENAME)
        run_info_filename = os.path.join(result_folder, RUN_INFO_FILENAME)

        features = read_from_json(features_filename)
        params = read_from_json(params_filename)
        run_info = read_from_json(run_info_filename)

        for i, vector_recipy in enumerate(recipes):
            #dep,octanol,octanoic,pentanol
            recipy = {}
            recipy['dep'] = vector_recipy[0]
            recipy['octanol'] = vector_recipy[1]
            recipy['octanoic'] = vector_recipy[2]
            recipy['pentanol'] = vector_recipy[3]

            if recipy == params['oil_formulation']:

                split_path = result_folder.split('/')
                identifier = '{}_{}'.format(split_path[-2], split_path[-1])
                save_folder = os.path.join(PLOT_FOLDER, str(i), identifier)
                plot_xp(save_folder, features, params, run_info)
