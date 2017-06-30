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

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})


if __name__ == '__main__':

    T = [20, 22, 24, 26, 27, 28]

    datasets = []
    for t in T:
        datasets.append(load_dataset(forge_dataset_filename_from_path('manual_exploration/temperature_analysis/experiments/{}'.format(t))))

    from datasets.datasets_tools import join_datasets

    datasets = join_datasets(*datasets)


    import numpy as np

    def unique_row(data):
        a = np.array(data)

        b = np.ascontiguousarray(a).view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
        _, idx = np.unique(b, return_index=True)

        unique_a = a[idx]

        return unique_a

    def get_row_idx(data, unique_row):
        return np.where((data == unique_row).all(axis=1))[0]


    X = np.array(datasets['droplet_composition']['vector_form'])
    unique_X = unique_row(X)

    for i in range(len(unique_X)):
        index = get_row_idx(X, unique_X[i,:])
        x = np.array(datasets['xp_info']['temperature'])[index]
        y = np.array(datasets['droplet_features']['average_speed'])[index]
        plt.figure()
        plt.scatter(x, y)
