import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

from datasets.datasets_tools import load_dataset
from datasets.datasets_tools import forge_dataset_filename_from_path
from datasets.datasets_tools import join_datasets
from datasets.datasets_tools import get_dataset_basepath

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from utils.plotting import save_and_close_fig

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})

N_REPEATS = 10
RECIPES_CSV_FILENAME = os.path.join(HERE_PATH, 'recipes_for_temperature_analysis.csv')
EXPERIMENT_FOLDER = os.path.join(HERE_PATH, 'experiments')

def load_recipes():
    data = np.loadtxt(RECIPES_CSV_FILENAME, delimiter=',', skiprows=1)
    # order is dep,octanol,octanoic,pentanol
    return data


# def unique_row(data):
#     a = np.array(data)
#     b = np.ascontiguousarray(a).view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
#     _, idx = np.unique(b, return_index=True)
#     unique_a = a[idx]
#     return unique_a

def find_row(X, row):
    return np.where((X == row).all(axis=1))[0]


if __name__ == '__main__':

    TEMPERATURE_DATA_RELPATH = 'manual_exploration/temperature_analysis/experiments'

    import filetools
    temperature_folders = filetools.list_folders(os.path.join(get_dataset_basepath(), TEMPERATURE_DATA_RELPATH))

    datasets = []
    for path in temperature_folders:
        datasets.append(load_dataset(forge_dataset_filename_from_path(path)))
    datasets = join_datasets(*datasets)

    ##
    X = np.array(datasets['droplet_composition']['vector_form'])
    recipes = load_recipes()

    PLOT_FOLDER = os.path.join(HERE_PATH, 'plots')
    filetools.ensure_dir(PLOT_FOLDER)

    for i in range(recipes.shape[0]):
        index = find_row(X, recipes[i,:])
        for k in datasets['droplet_features'].keys():
            x = np.array(datasets['xp_info']['temperature'])[index]
            y = np.array(datasets['droplet_features'][k])[index]

            fig = plt.figure(figsize=(12,8))
            plt.scatter(x, y, 50, 'b')
            # plt.plot(x, y_rbf, 'k')
            plt.xlabel('Temperature', fontsize=fontsize)
            plt.ylabel(k, fontsize=fontsize)
            plt.xlim([15, 30])
            delta_y = 0.1*(np.max(y) - np.min(y))
            plt.ylim([np.min(y)-delta_y, np.max(y)+delta_y])
            plt.title(str(datasets['droplet_composition']['norm_json_form'][index[0]]))
            plt.tight_layout()

            i_plot_folder = os.path.join(PLOT_FOLDER, str(i))
            filetools.ensure_dir(i_plot_folder)
            plotfilebasename = os.path.join(i_plot_folder, k)
            save_and_close_fig(fig, plotfilebasename, exts=['.png'])


    for k in ['average_speed', 'average_number_of_droplets']:
        for i, ind in enumerate([2, 3, 4]):
            index = find_row(X, recipes[ind,:])
            x = np.array(datasets['xp_info']['temperature'])[index]
            y = np.array(datasets['droplet_features'][k])[index]

            sorted_ind = np.argsort(x)
            x = x[sorted_ind]
            y = y[sorted_ind]

            from sklearn.svm import SVR
            x = x.reshape([x.size, 1])

            svr_rbf = SVR(kernel='rbf', C=1, gamma=0.2)
            y_rbf = svr_rbf.fit(x, y).predict(x
            )

            fig = plt.figure(figsize=(8,8))
            plt.scatter(x, y, 20, c=['b', 'g', 'r'][i])
            plt.plot(x, y_rbf, c=['b', 'g', 'r'][i])

            plt.xlabel('Temperature - C', fontsize=fontsize)
            plt.xlim([17, 30])
            if k == 'average_speed':
                plt.ylim([0, 20])
                plt.ylabel('Avg Speed - mm/s', fontsize=fontsize)
            else:
                plt.ylim([0, 15])
                plt.ylabel('Avg Nb of Droplets', fontsize=fontsize)
            plt.tight_layout()

            plotfilebasename = os.path.join(PLOT_FOLDER, k + '_' + str(ind))
            save_and_close_fig(fig, plotfilebasename, exts=['.png'])


    # ##
    # index = find_row(X, recipes[3,:])
    # x = np.array(datasets['droplet_features']['average_speed'])[index]
    # low = x > 0
    # high = x < 2
    # ind = np.logical_and(low, high)
    # print np.array(datasets['paths'])[index[ind]]

    # ##
    # from scipy.interpolate import UnivariateSpline
    # x = np.array(datasets['xp_info']['temperature'])[index]
    # y = np.array(datasets['droplet_features']['average_speed'])[index]
    #
    # ind = np.argsort(x)
    # x = x[ind]
    # y = y[ind]
    #
    # from sklearn.svm import SVR
    # X = x.reshape([x.size, 1])
    #
    # svr_rbf = SVR(kernel='rbf', C=1, gamma=0.1)
    # y_rbf = svr_rbf.fit(X, y).predict(X)
    #
    # fig = plt.figure(figsize=(12,8))
    # plt.scatter(x, y, 50, 'b')
    # plt.plot(x, y_rbf)
    # plt.ylim([-1, 20])
