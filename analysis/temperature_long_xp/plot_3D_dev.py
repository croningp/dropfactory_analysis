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
from mpl_toolkits.mplot3d import Axes3D
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

# PLOT_FOLDER = os.path.join(HERE_PATH, 'plots')
# filetools.ensure_dir(PLOT_FOLDER)

CSV_PATH = os.path.join(HERE_PATH, 'csv')


def load_csv(path):
    return np.loadtxt(path, skiprows=1)

if __name__ == '__main__':

    files = filetools.list_files(CSV_PATH, ['*.csv'])

    # path = '/home/group/workspace/dropfactory_analysis/analysis/temperature_long_xp/csv/3/average_number_of_droplets.csv'
    path = '/home/group/workspace/dropfactory_analysis/analysis/temperature_long_xp/csv/3/average_speed.csv'
    # path = '/home/group/workspace/dropfactory_analysis/analysis/temperature_long_xp/csv/3/average_area.csv'

    data = load_csv(path)


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    cmhot = plt.get_cmap("jet")

    step = 1
    # color = np.clip(data[0:-1:step, 2], 0, 10)
    color = np.clip(data[0:-1:step, 2], 0, np.inf)

    # plt.scatter(data[0:-1:step, 0], data[0:-1:step, 1], 50, c=color, cmap=cmhot)
    ax.scatter(data[0:-1:step, 0], data[0:-1:step, 1], data[0:-1:step, 2], c=color, cmap=cmhot)

    plt.colorbar()
