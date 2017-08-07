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

from utils.tools import save_to_json
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

    datasets = load_temperature_dataset()

    ##
    XP = np.array(datasets['droplet_composition']['vector_form'])
    recipes = load_recipes()

    PLOT_FOLDER = os.path.join(HERE_PATH, 'plots')
    filetools.ensure_dir(PLOT_FOLDER)

    feature_names = datasets['droplet_features'].keys()

    for i in range(recipes.shape[0]):
        print 'Recipe: {}'.format(i)
        index = find_row(XP, recipes[i,:])
        for r in range(1, len(feature_names)):
            print 'Number of features: {}'.format(r)
            for comb_number, comb in enumerate(combinations(feature_names, r)):

                ## set a seed for reproducible results
                set_seed(0, verbose=False)

                # check not already done, skip if done
                # delete files if you want to recompute it all or comment below section
                DATA_FOLDER = os.path.join(HERE_PATH, 'data', str(i), str(r))
                filetools.ensure_dir(DATA_FOLDER)
                datafilename = os.path.join(DATA_FOLDER, '{}.json'.format(comb_number))

                PLOT_FOLDER = os.path.join(HERE_PATH, 'plots', str(i), str(r))
                filetools.ensure_dir(PLOT_FOLDER)
                plotfilebasename = os.path.join(PLOT_FOLDER, str(comb_number))

                if os.path.exists(datafilename) and os.path.exists('{}.png'.format(plotfilebasename)):
                    continue

                ## make datasets
                X = []
                for k in comb:
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

                ## collect results
                data = {}
                data['features'] = comb
                data['y'] = y.tolist()
                data['y_pred'] = y_pred.tolist()
                data['mean_absolute_error'] = mean_absolute_error(y, y_pred)
                data['mean_squared_error'] = mean_squared_error(y, y_pred)
                data['median_absolute_error'] = median_absolute_error(y, y_pred)
                ## save data
                save_to_json(data, datafilename)

                ## plotting
                fig = plt.figure(figsize=(8,8))
                plt.plot([15, 30], [15, 30], 'k--')
                plt.scatter(y, y_pred, 50)
                plt.xlabel('Measured Temperature - C', fontsize=fontsize)
                plt.ylabel('Predicted Temperature - C', fontsize=fontsize)
                plt.tight_layout()
                ## save plot
                save_and_close_fig(fig, plotfilebasename, exts=['.png'])
