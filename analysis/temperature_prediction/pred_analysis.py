import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

import numpy as np
from scipy.stats.stats import pearsonr

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import filetools

from utils.tools import read_from_json

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})

if __name__ == '__main__':

    DATA_FOLDER = os.path.join(HERE_PATH, 'data')

    fig = plt.figure(figsize=(12, 8))

    for recipe_nb in range(2,3):
        min_error_curve = []
        min_nb_curve = []
        min_residual_mean = []
        min_residual_std = []
        R = []
        for comb_nb in range(1, 11):
            data_folder = os.path.join(DATA_FOLDER, str(recipe_nb), str(comb_nb))

            data_files = filetools.list_files(data_folder)

            errors = []
            residuals_mean = []
            residuals_std = []
            rs = []
            for data_file in data_files:
                data = read_from_json(data_file)
                errors.append(data['mean_squared_error'])

                er = np.array(data['y_pred']) - np.array(data['y'])
                residuals_mean.append(np.mean(er))
                residuals_std.append(np.std(er))
                rs.append(pearsonr(data['y'], data['y_pred']))

            min_error_curve.append(np.min(errors))
            min_nb_curve.append(data_files[np.argmin(errors)])
            min_residual_mean.append(residuals_mean[np.argmin(errors)])
            min_residual_std.append(residuals_std[np.argmin(errors)])
            R.append(rs[np.argmin(errors)])

        plt.plot(min_error_curve)

    plt.show()

    
