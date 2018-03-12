import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..')
sys.path.append(root_path)

DROPFACTORY_UTILS_PATH = os.path.join(HERE_PATH, '..', 'dropfactory_exploration', 'utils')

# ORKNEY_XP_FOLDER = '/home/group/orkney1/Chemobot/dropfactory_exploration/realworld_experiments/'
ORKNEY_XP_FOLDER = '/media/jgrizou/FULL_CRONIN/ORKNEY/dropfactory_exploration/realworld_experiments'

DATASET_FILENAME = 'data.json'
REPEATS_FILENAME = 'repeats.json'
