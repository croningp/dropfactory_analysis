import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..')
sys.path.append(root_path)

from datasets.datasets_tools import build_csv
from datasets.datasets_tools import get_dataset_basepath
from datasets.datasets_tools import load_dataset
from datasets.datasets_tools import join_datasets

import filetools

if __name__ == '__main__':

    DATASET_PATH = get_dataset_basepath()
    dataset_filenames = filetools.list_files(DATASET_PATH, ['data.json'])

    full_dataset = None

    for filename in dataset_filenames:
        data = load_dataset(filename)

        if full_dataset is None:
            full_dataset = data
        else:
            full_dataset = join_datasets(full_dataset, data)

        # buld file name
        rel_path = os.path.relpath(filename, DATASET_PATH)
        base_rel_path, ext = os.path.splitext(rel_path)
        csv_filename = os.path.join(HERE_PATH, base_rel_path + '.csv')

        ## save
        filetools.ensure_dir(os.path.split(csv_filename)[0])  # ensure folder
        build_csv(data, csv_filename)

    ##
    full_csv_filename = os.path.join(HERE_PATH, 'full.csv')
    build_csv(full_dataset, full_csv_filename)
