import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '../../..')
sys.path.append(root_path)

from datasets.datasets_tools import load_dataset
from datasets.datasets_tools import forge_dataset_filename

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})


METHOD_NAMES = ['random_params', 'random_goal']
SEEDS = ['110', '111', '112']
X_FEATURE_NAME = 'average_speed'
Y_FEATURE_NAME = 'average_number_of_droplets'
COLORS = ['b', 'r']

import numpy as np
from utils.plotting import plot_kde

if __name__ == '__main__':

    N_METHODS = len(METHOD_NAMES)
    N_SEEDS = len(SEEDS)

    fig  = plt.figure(figsize=(N_SEEDS*8, N_METHODS*8))

    for i_method_name, method_name in enumerate(METHOD_NAMES):
        for i_seed, seed in enumerate(SEEDS):
            plt.subplot(N_METHODS, N_SEEDS, i_method_name*N_SEEDS + i_seed + 1)

            if method_name != 'random_params':
                seed = '{}_speed_division'.format(seed)
            data = load_dataset(forge_dataset_filename(method_name, seed))
            x = data['droplet_features'][X_FEATURE_NAME]
            y = data['droplet_features'][Y_FEATURE_NAME]

            kde_data = np.array([x, y])
            cmap = plt.cm.jet
            plot_kde(kde_data, bounds = [0, 20, 0, 20], bandwidth=0.3, cmap=cmap)
            plt.colorbar()
            # plt.clim(0, 0.1)
            plt.xlabel('Speed', fontsize=fontsize)
            plt.ylabel('Division', fontsize=fontsize)
            plt.tight_layout()

    ##
    import filetools
    from utils.plotting import save_and_close_fig

    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    figure_filebasename = os.path.join(plot_folder, 'density')
    save_and_close_fig(fig, figure_filebasename)
