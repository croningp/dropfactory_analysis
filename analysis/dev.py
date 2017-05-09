import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..')
sys.path.append(root_path)

from datasets.datasets_tools import load_repeats
from datasets.datasets_tools import forge_repeats_filename

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})


if __name__ == '__main__':

    t = 2
    repeats = load_repeats(forge_repeats_filename('random_goal', '11{}_speed_division'.format(t)))

    for repeat in repeats:
        x = repeat['droplet_features']['average_speed']
        y = repeat['droplet_features']['average_number_of_droplets']

        import numpy as np
        mean_x = np.mean(x)
        std_x = np.std(x)
        mean_y = np.mean(y)
        std_y = np.std(y)

        # plt.plot([x[0], mean_x], [y[0], mean_y], 'k--')
        # plt.scatter(x[0], y[0], 50, c='r')
        plt.errorbar(mean_x, mean_y, yerr=std_y, xerr=std_x, fmt='o', ecolor='g', capthick=2)

    plt.xlabel('Speed', fontsize=fontsize)
    plt.ylabel('Division', fontsize=fontsize)
    plt.tight_layout()
