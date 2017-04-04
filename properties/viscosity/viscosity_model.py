import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
properties_folder = os.path.join(HERE_PATH, '..')
sys.path.append(properties_folder)

import numpy as np

from properties_constants import MEASURED_DENSITIES
from properties_constants import MEASURED_VISCOSITIES
from properties_constants import MOLECULAR_WEIGHTS

from tools import ratio_normalize
from tools import load_model


def compute_formula_viscosities(oil_ratios):
    # check data are in ratio form
    np.testing.assert_array_almost_equal(np.sum(oil_ratios, axis=1), 1, decimal=2)

    mole_factor = MEASURED_DENSITIES / MOLECULAR_WEIGHTS
    mole_fraction = ratio_normalize(oil_ratios * mole_factor)
    log_viscosities = np.log(MEASURED_VISCOSITIES)
    return np.ravel(np.exp(np.dot(mole_fraction, log_viscosities.T)))


def compute_regression_viscosities(oil_ratios):
    # check data are in ratio form
    np.testing.assert_array_almost_equal(np.sum(oil_ratios, axis=1), 1, decimal=2)

    model_filename = os.path.join(HERE_PATH, 'regressor_info', 'model.pkl')
    model = load_model(model_filename)

    return model.predict(oil_ratios)
