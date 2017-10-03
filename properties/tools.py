import os

import json
import pickle
import multiprocessing

import random
import numpy as np

from sklearn.svm  import SVR
from sklearn.grid_search import GridSearchCV

import filetools


def set_seed(seed, verbose=True):
    if verbose:
        print 'Setting seed to {}'.format(seed)
    random.seed(seed)
    np.random.seed(seed)


def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)


def ratio_normalize(x):
    x = np.array(x, dtype=float)
    div = np.sum(x, 1)
    norm_x = x / div[:, None]
    norm_x[np.where(div == 0)[0]] = 1.0 / x.shape[1]
    return norm_x


def load_csv(filename):
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    # ["DEP", "1-Octanol", "Octanoic-Acid", "1-Pentanol"]
    #csv data must be in that order: DEP, 1-Octanol, Octanoic-Acid, 1-Pentanol, property
    return data[:,0:4], data[:, 4]


def cv_train_svr(X, y, n_jobs=multiprocessing.cpu_count()):

    param_grid = {'kernel': ['rbf'],
                  'C': np.logspace(-2, 2, 21),
                  'gamma': np.logspace(-2, 2, 21)
                 }

    model = GridSearchCV(SVR(), param_grid, scoring='mean_squared_error', cv=10, n_jobs=n_jobs)

    model.fit(X, y)

    return model


def save_model(model, filename):
    filetools.ensure_dir(os.path.dirname(filename))
    pickle.dump(model, open(filename, "wb"))


def load_model(filename):
    return pickle.load(open(filename))
