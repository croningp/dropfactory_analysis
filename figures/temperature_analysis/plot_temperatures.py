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

from utils.temperature_tools import load_temperature_dataset
from utils.temperature_tools import load_recipes
from utils.temperature_tools import find_row

from sklearn.svm import SVR

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})

TEMPERATURE_LABEL = 'Temperature / $^{\circ}C$'
SPEED_LABEL = 'Average Speed of Droplets / $mm.s^{-1}$'
DIVISION_LABEL = 'Average Number of Droplets'

current_palette = sns.color_palette()
COLORS = [current_palette[1], current_palette[3]]

if __name__ == '__main__':

    datasets = load_temperature_dataset()

    ##
    X = np.array(datasets['droplet_composition']['vector_form'])
    recipes = load_recipes()

    PLOT_FOLDER = os.path.join(HERE_PATH, 'plots')
    filetools.ensure_dir(PLOT_FOLDER)

    for k in ['average_speed', 'average_number_of_droplets']:
        for i, ind in enumerate([2, 3]):
            index = find_row(X, recipes[ind,:])
            x = np.array(datasets['xp_info']['temperature'])[index]
            y = np.array(datasets['droplet_features'][k])[index]

            sorted_ind = np.argsort(x)
            x = x[sorted_ind]
            y = y[sorted_ind]

            x = x.reshape([x.size, 1])

            svr_rbf = SVR(kernel='rbf', C=1, gamma=0.2)
            y_rbf = svr_rbf.fit(x, y).predict(x)

            ##
            fig = plt.figure(figsize=(8,8))
            with sns.axes_style("ticks"):
                ax = plt.subplot(111)

            plt.scatter(x, y, 100, c=COLORS[i])
            # plt.plot(x, y_rbf, c=COLORS[i], linestyle='--', linewidth=4)

            plt.xlabel(TEMPERATURE_LABEL, fontsize=fontsize)

            if k == 'average_speed':
                plt.ylim([0, 20])
                plt.ylabel(SPEED_LABEL, fontsize=fontsize)
            else:
                plt.ylim([0, 20])
                plt.ylabel(DIVISION_LABEL, fontsize=fontsize)

            plt.xlim([17, 30])
            xticks = [17, 20, 25, 30]
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticks)

            sns.despine(offset=10, trim=True, ax=ax)
            plt.tight_layout()

            plotfilebasename = os.path.join(PLOT_FOLDER, k + '_' + str(ind))
            save_and_close_fig(fig, plotfilebasename)
