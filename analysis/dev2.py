import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..')
sys.path.append(root_path)

from datasets.datasets_tools import forge_dataset_filename
from datasets.datasets_tools import load_dataset

from utils.tools import read_from_json

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})


if __name__ == '__main__':

    data = load_dataset(forge_dataset_filename('random_goal', '110_speed_division'))

    raw_data = read_from_json(forge_dataset_filename('random_goal', '110_speed_division'))
