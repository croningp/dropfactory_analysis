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

from itertools import combinations

import filetools

from utils.plotting import save_and_close_fig

from utils.temperature_tools import load_temperature_dataset
from utils.temperature_tools import load_recipes
from utils.temperature_tools import find_row

from utils.seed import set_seed

import multiprocessing
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVR
from sklearn import preprocessing
from sklearn.cross_validation import LeaveOneOut

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import median_absolute_error

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})

if __name__ == '__main__':

    ## set a seed for reproducible results
    set_seed(0, verbose=False)

    datasets = load_temperature_dataset()

    ##
    XP = np.array(datasets['droplet_composition']['vector_form'])
    recipes = load_recipes()

    PLOT_FOLDER = os.path.join(HERE_PATH, 'plots')
    filetools.ensure_dir(PLOT_FOLDER)

    ##
    RECIPE_NUMBER = 2
    FEATURES_NAME = ['covered_arena_area', 'total_droplet_path_length']

    index = find_row(XP, recipes[RECIPE_NUMBER,:])

    ## make datasets
    X = []
    for k in FEATURES_NAME:
        X.append(np.array(datasets['droplet_features'][k])[index])
    X = np.array(X).T
    ## scale X to 0 mean and 1 std
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)

    y = np.array(datasets['xp_info']['temperature'])[index]

    ## estimate best clf params on the all dataset
    model_info = {'estimator': SVR(kernel='rbf'),
                  'param_grid': {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                                 'gamma': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}}

    clf = GridSearchCV(model_info['estimator'], model_info['param_grid'], scoring='mean_squared_error', cv=10, n_jobs=multiprocessing.cpu_count())
    clf.fit(X, y)
    best_params = clf.best_params_

    ## make the final estimate using leave one out, just to always test on never seen data
    ## this is what would happen to predict temperature from a new droplet experiment never done before
    y_pred = np.zeros(np.shape(y)) * np.nan
    for train_index, test_index in LeaveOneOut(X.shape[0]):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        ## Note that we retrain a new model each time here from the train data, and test it on the remaining, we just use the best parameters for the SVR estimated earlier
        ## Ideally we would want to run GridSearchCV in each loop but that would take forever and not make a difference
        best_clf = SVR(kernel='rbf', **best_params)
        y_pred[test_index] = best_clf.fit(X_train, y_train).predict(X_test)

    # just checking it all went fine
    assert(not np.any(np.isnan(y_pred)))

    residual = y_pred - y
    mean_residual = np.mean(residual)
    std_residual = np.std(residual)

    ## plotting

    LIM_TEMP = [17, 30]
    LIM_RES = [-2.5, 2.5]
    COLOR = sns.color_palette(["#34495e"])[0]

    fig = plt.figure(figsize=(10,12))
    with sns.axes_style("ticks"):
        ax1 = plt.subplot2grid((6, 5), (0, 0), colspan=4, rowspan=4)
    with sns.axes_style("ticks"):
        ax2 = plt.subplot2grid((6, 5), (4, 0), colspan=4, rowspan=2)
    with sns.axes_style("ticks"):
        ax3 = plt.subplot2grid((6, 5), (4, 4), colspan=1, rowspan=2)

    ax1.scatter(y, y_pred, 150, c=COLOR)
    ax1.plot(LIM_TEMP, LIM_TEMP, color=COLOR, linestyle='--')
    ax1.set_xlabel('Measured Temperature / $^{\circ}C$', fontsize=fontsize)
    ax1.set_ylabel('Predicted Temperature / $^{\circ}C$', fontsize=fontsize)

    ax1.set_xlim(LIM_TEMP)
    ax1.set_ylim(LIM_TEMP)

    ticks = [17, 20, 25, 30]
    ax1.set_xticks(ticks)
    ax1.set_xticklabels(ticks)
    ax1.set_yticks(ticks)
    ax1.set_yticklabels(ticks)
    sns.despine(offset=10, trim=True, ax=ax1)

    ##
    ax2.scatter(y, residual, 150, c=COLOR)
    ax2.plot(LIM_TEMP, [0, 0], color=COLOR, linestyle='--')

    ax2.set_xlabel('Measured Temperature / $^{\circ}C$', fontsize=fontsize)
    ax2.set_ylabel('Residual', fontsize=fontsize)

    ax2.set_xlim(LIM_TEMP)
    ax2.set_ylim(LIM_RES)

    xticks = [17, 20, 25, 30]
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xticks)
    yticks = [-2, 0, 2]
    ax2.set_yticks(yticks)
    ax2.set_yticklabels(yticks)

    sns.despine(offset=10, trim=True, ax=ax2)

    ##
    from scipy.stats import norm

    x_dist = np.linspace(LIM_RES[0], LIM_RES[1], 100)
    y_dist = norm.pdf(x_dist, mean_residual, std_residual)
    sns.distplot(a=residual, kde=False, fit=norm, vertical=True, color=COLOR)
    ax3.set_ylim(LIM_RES)

    sns.despine(left=True, bottom=True, ax=ax3)

    ax3.set_xticks([])
    ax3.set_xticklabels([])
    ax3.set_yticks([])
    ax3.set_yticklabels([])

    plt.tight_layout()

    ## save plot
    plotfilebasename = os.path.join(PLOT_FOLDER, 'temp_prediction')
    save_and_close_fig(fig, plotfilebasename, exts=['.png'])
