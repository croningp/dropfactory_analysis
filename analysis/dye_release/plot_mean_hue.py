import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

from utils.tools import read_from_json

import numpy as np

import filetools

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})


def get_all_hues_in_folder(path):
    hue_files = filetools.list_files(path, ['mean_hue.json'])
    all_hues = []
    for hue_file in hue_files:
        results = read_from_json(hue_file)
        all_hues.append(results['mean_hue'][0:5900])
    return np.array(all_hues)

if __name__ == '__main__':

    DATA_PATH = os.path.join(HERE_PATH, 'data')

    COLD_XP_PATH = os.path.join(DATA_PATH, 'AC_19.0_LJP5-22-Ey')
    cold_hues = get_all_hues_in_folder(COLD_XP_PATH)

    HOT_XP_PATH = os.path.join(DATA_PATH, 'AC_28_LJP5-22-Ey')
    hot_hues = get_all_hues_in_folder(HOT_XP_PATH)

    plt.plot(np.mean(cold_hues, axis=0), 'b')
    plt.plot(np.mean(hot_hues, axis=0), 'r')

    plt.xlabel('Frame', fontsize=fontsize)
    plt.ylabel('Dye Release', fontsize=fontsize)

    plt.legend(['19 C', '28 C'], fontsize=fontsize, loc=4)

    plt.tight_layout()
