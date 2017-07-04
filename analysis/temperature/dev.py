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

    # for i in range(recipes.shape[0]):
    #     index = find_row(X, recipes[i,:])
    #     x = np.array(datasets['xp_info']['temperature'])[index]
    #     y1 = np.array(datasets['droplet_features']['average_speed'])[index]
    #     y2 = np.array(datasets['droplet_features']['ratio_frame_active'])[index]
    #     y3 = np.array(datasets['droplet_features']['average_number_of_droplets'])[index]
    #
    #     fig = plt.figure(figsize=(12,8))
    #     plt.scatter(x, y1, 50, 'b')
    #     plt.scatter(x, y2, 50, 'r')
    #     plt.scatter(x, y3, 50, 'g')
    #     plt.legend(['Speed', 'Lifetime', 'Division'])
    #     plt.xlabel('Temperature', fontsize=fontsize)
    #     plt.title(str(datasets['droplet_composition']['norm_json_form'][index[0]]))
    #
    #     plotfilebasename = os.path.join(PLOT_FOLDER, str(i))
    #     save_and_close_fig(fig, plotfilebasename, exts=['.png'])


    index = find_row(X, recipes[3,:])
    x = np.array(datasets['droplet_features']['average_speed'])[index]
    low = x > 0
    high = x < 2
    ind = np.logical_and(low, high)

    # print np.array(datasets['paths'])[index[ind]]

    ##
    from scipy.interpolate import UnivariateSpline
    x = np.array(datasets['xp_info']['temperature'])[index]
    y = np.array(datasets['droplet_features']['average_speed'])[index]

    ind = np.argsort(x)
    x = x[ind]
    y = y[ind]

    from scipy import interpolate

    spl = UnivariateSpline(x, y)
    spl.set_smoothing_factor(0.1)
    xs = np.linspace(15, 30, 1000)
    ys = spl(xs)

    f = interpolate.interp1d(x, y)
    yf = f(x)

    from sklearn.svm import SVR
    X = x.reshape([x.size, 1])

    svr_rbf = SVR(kernel='rbf', C=1, gamma=0.1)
    y_rbf = svr_rbf.fit(X, y).predict(X)

    fig = plt.figure(figsize=(12,8))
    plt.scatter(x, y, 50, 'b')
    plt.plot(x, y_rbf)
    plt.ylim([-1, 20])
