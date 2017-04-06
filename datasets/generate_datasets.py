import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..')
sys.path.append(root_path)

from constants import DROPFACTORY_UTILS_PATH
sys.path.append(DROPFACTORY_UTILS_PATH)

#
from xp_utils import XPTools

from filenaming import XP_PARAMS_FILENAME
from filenaming import XP_FEATURES_FILENAME
from filenaming import EXPLAUTO_INFO_FILENAME
from filenaming import RUN_INFO_FILENAME
from filenaming import DROPLET_FEATURES_FILENAME

def read_all_xp(pool_folder):

    xptool = XPTools(pool_folder)

    data = {}
    data['info'] = xptool.info_dict

    data['experiments'] = []
    for ixp in range(xptool.info_dict['n_xp_total']):
        xp_data = {}

        xp_data['params'] = xptool.get_json_content_from_xp_number_and_filename(ixp, XP_PARAMS_FILENAME)
        xp_data['features'] = xptool.get_json_content_from_xp_number_and_filename(ixp, XP_FEATURES_FILENAME)
        xp_data['explauto_info'] = xptool.get_json_content_from_xp_number_and_filename(ixp, EXPLAUTO_INFO_FILENAME)
        xp_data['droplet_features'] = xptool.get_json_content_from_xp_number_and_filename(ixp, DROPLET_FEATURES_FILENAME)
        xp_data['run_info'] = xptool.get_json_content_from_xp_number_and_filename(ixp, RUN_INFO_FILENAME)
        xp_data['valid'] = xptool.is_xp_performed(ixp)

        data['experiments'].append(xp_data)

    return data


##
import filetools
from utils.tools import save_to_json
from constants import DATASET_FILENAME

def gather_and_save_pool_folder(pool_folder):


    rel_path = os.path.relpath(pool_folder, ORKNEY_XP_FOLDER)
    save_folder = os.path.join(HERE_PATH, rel_path)
    filetools.ensure_dir(save_folder)

    save_filename = os.path.join(save_folder, DATASET_FILENAME)

    if os.path.exists(save_filename):
        print 'Skipping {} already generated'.format(rel_path)
        return

    # else do the stuff
    print 'Working on {}'.format(rel_path)
    data = read_all_xp(pool_folder)
    save_to_json(data, save_filename)


if __name__ == '__main__':

    from constants import ORKNEY_XP_FOLDER

    POOL_FOLDERS = []
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '100'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '101'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '110'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '111'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '112'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_goal', '110_speed_deformation'))

    for pool_folder in POOL_FOLDERS:
        gather_and_save_pool_folder(pool_folder)
