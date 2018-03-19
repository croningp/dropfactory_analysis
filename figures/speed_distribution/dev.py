import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '../..')
sys.path.append(root_path)

from datasets.datasets_tools import load_dataset
from datasets.datasets_tools import forge_dataset_filename

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np

import filetools
from utils.plotting import save_and_close_fig

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})

if __name__ == '__main__':

    X_FEATURE_NAME = 'average_speed'
    METHOD_NAMES = ['random_params', 'random_goal']
    SEED_HOT = ['110', '111', '112']
    SEED_COLD = ['210', '211', '212']
    SEEDS_SET = [SEED_HOT, SEED_COLD]

    N_METHODS = len(METHOD_NAMES)

    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    plt.ion()

    #
    DATA = {}
    for i_method_name, method_name in enumerate(METHOD_NAMES):

        # fig = plt.figure()

        DATA[method_name] = {}
        for seed_set in SEEDS_SET:
            seed_set_speeds = []
            for i_seed, seed in enumerate(seed_set):
                DATA[method_name][seed] = {}

                dataset_seed = seed
                if method_name != 'random_params':
                    dataset_seed = '{}_speed_division'.format(seed)
                data = load_dataset(forge_dataset_filename(method_name, dataset_seed))

                speeds = np.array(data['droplet_features'][X_FEATURE_NAME])

                seed_set_speeds.append(speeds)

            datfit = np.array(seed_set_speeds).ravel()
            # sns.kdeplot(datfit, gridsize=100, cumulative=True)
            # sns.kdeplot(np.array(seed_set_speeds).ravel(), gridsize=1000)

            from statsmodels.nonparametric.kde import KDEUnivariate
            kde = KDEUnivariate(datfit)
            kde.fit()

            plt.plot(kde.support, 1-kde.cdf)

            # raw_input()
            # plt.close()

        plt.xlim([0, 15])
        # plt.ylim([0, 1.5])
