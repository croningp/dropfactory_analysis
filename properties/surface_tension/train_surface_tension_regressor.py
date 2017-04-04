import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
properties_folder = os.path.join(HERE_PATH, '..')
sys.path.append(properties_folder)

from tools import load_csv
from tools import cv_train_svr
from tools import save_model
from tools import save_to_json
from tools import set_seed

if __name__ == '__main__':

    set_seed(0)

    csv_filename = os.path.join(HERE_PATH, 'surface_tension_data.csv')

    X, y = load_csv(csv_filename)
    model = cv_train_svr(X, y)

    regressor_folder = os.path.join(HERE_PATH, 'regressor_info')
    pickled_filename = os.path.join(regressor_folder, 'model.pkl')
    save_model(model, pickled_filename)

    param_filename = os.path.join(regressor_folder, 'params.json')
    save_to_json(model.best_params_, param_filename)
