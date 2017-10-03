import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

from utils.temperature_tools import load_temperature_dataset
from utils.temperature_tools import load_recipes
from utils.temperature_tools import find_row

from datasets.datasets_tools import build_csv

import filetools

if __name__ == '__main__':


    dataset = load_temperature_dataset()

    save_dir = os.path.join(HERE_PATH, 'csv')
    filetools.ensure_dir(save_dir)

    #
    import numpy as np
    from datasets.datasets_tools import sub_dataset

    X = np.array(dataset['droplet_composition']['vector_form'])
    recipes = load_recipes()

    for i in range(recipes.shape[0]):
        index = find_row(X, recipes[i,:])

        sub_data = sub_dataset(dataset, index)

        filename =  os.path.join(save_dir, '{}.csv'.format(i))
        build_csv(sub_data, filename)
