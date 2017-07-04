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
from filenaming import REPEATS_FOLDERNAME
from filenaming import REPEATS_INFO_FILENAME

import filetools
from utils.tools import save_to_json
from constants import DATASET_FILENAME
from constants import REPEATS_FILENAME

FOLDERNAME_N_DIGIT = 2
FOLDERNAME_SPACE_CHAR = '_'


def collect_xp_data_from_folder(pool_folder, xp_folder):
    xptool = XPTools(pool_folder)

    xp_data = {}
    xp_data['path'] = os.path.join(pool_folder, xp_folder)
    xp_data['params'] = xptool.get_json_content_from_xp_folder_and_filename(xp_folder, XP_PARAMS_FILENAME)
    xp_data['features'] = xptool.get_json_content_from_xp_folder_and_filename(xp_folder, XP_FEATURES_FILENAME)
    xp_data['explauto_info'] = xptool.get_json_content_from_xp_folder_and_filename(xp_folder, EXPLAUTO_INFO_FILENAME)
    xp_data['droplet_features'] = xptool.get_json_content_from_xp_folder_and_filename(xp_folder, DROPLET_FEATURES_FILENAME)
    xp_data['run_info'] = xptool.get_json_content_from_xp_folder_and_filename(xp_folder, RUN_INFO_FILENAME)

    return xp_data


def read_all_xp(pool_folder):
    xptool = XPTools(pool_folder)

    data = {}
    data['info'] = xptool.info_dict

    data['experiments'] = []
    for ixp in range(xptool.info_dict['n_xp_total']):
        xp_folder = xptool.generate_XP_foldername(ixp)
        xp_data = collect_xp_data_from_folder(pool_folder, xp_folder)
        data['experiments'].append(xp_data)

    return data


def generate_repeat_xp_folder(root_path, i_xp, i_repeat):
    i_xp_str = filetools.generate_n_digit_name(i_xp, n_digit=FOLDERNAME_N_DIGIT)
    i_repeat_str = filetools.generate_n_digit_name(i_repeat, n_digit=FOLDERNAME_N_DIGIT)
    foldername = i_xp_str + FOLDERNAME_SPACE_CHAR + i_repeat_str
    return os.path.join(root_path, foldername)


def read_all_repeats(pool_folder):
    xptool = XPTools(pool_folder)
    repeats = {}

    repeats_folder = os.path.join(pool_folder, REPEATS_FOLDERNAME)
    if not os.path.exists(repeats_folder):
        rel_path = os.path.relpath(pool_folder, ORKNEY_XP_FOLDER)
        print 'Skipping {} repeats not run'.format(rel_path)
        return repeats

    ##
    repeats['info'] = xptool.get_json_content_from_xp_folder_and_filename(repeats_folder, REPEATS_INFO_FILENAME)

    n_xp_repeated = repeats['info']['n_xp']
    n_repeats = repeats['info']['n_repeats']
    xp_repeated_number = repeats['info']['xp_number']

    repeats['experiments'] = []
    for i_xp_repeated in range(n_xp_repeated):

        xp_number = xp_repeated_number[i_xp_repeated]
        xp_folder = xp_folder = xptool.generate_XP_foldername(xp_number)
        original_xp_data = collect_xp_data_from_folder(pool_folder, xp_folder)

        ## repeats
        repeat_xp_data = []
        for i_repeats in range(n_repeats):
            xp_folder = generate_repeat_xp_folder(repeats_folder, i_xp_repeated, i_repeats)
            xp_data = collect_xp_data_from_folder(pool_folder, xp_folder)
            repeat_xp_data.append(xp_data)

        ##
        repeat_data = {}
        repeat_data['original'] = original_xp_data
        repeat_data['repeats'] = repeat_xp_data

        repeats['experiments'].append(repeat_data)

    return repeats


def gather_and_save_pool_folder(pool_folder):

    rel_path = os.path.relpath(pool_folder, ORKNEY_XP_FOLDER)
    save_folder = os.path.join(HERE_PATH, rel_path)
    filetools.ensure_dir(save_folder)

    # data
    data_filename = os.path.join(save_folder, DATASET_FILENAME)

    if os.path.exists(data_filename):
        print 'Skipping {} data already extracted'.format(rel_path)
    else:
        # else do the stuff
        print 'Working on data from {}'.format(rel_path)
        data = read_all_xp(pool_folder)
        save_to_json(data, data_filename)

    # repeats
    repeats_filename = os.path.join(save_folder, REPEATS_FILENAME)

    if os.path.exists(repeats_filename):
        print 'Skipping {} repeats already extracted'.format(rel_path)
    else:
        # else do the stuff
        print 'Working on repeats from {}'.format(rel_path)
        repeats = read_all_repeats(pool_folder)
        save_to_json(repeats, repeats_filename)


if __name__ == '__main__':

    from constants import ORKNEY_XP_FOLDER

    POOL_FOLDERS = []
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '100'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '101'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '110'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '111'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '112'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_goal', '110_speed_deformation'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_goal', '110_speed_division'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_goal', '111_speed_division'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_goal', '112_speed_division'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'grid_search', '5'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'grid_search', '6'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'reach', '110_speed_division'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'reach', '111_speed_division'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'reach', '112_speed_division'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'manual_exploration', 'temperature_analysis', 'experiments', '20'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'manual_exploration', 'temperature_analysis', 'experiments', '22'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'manual_exploration', 'temperature_analysis', 'experiments', '24'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'manual_exploration', 'temperature_analysis', 'experiments', '26'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'manual_exploration', 'temperature_analysis', 'experiments', '27'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'manual_exploration', 'temperature_analysis', 'experiments', '28'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'manual_exploration', 'temperature_analysis', 'experiments', 'no_control_1'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'manual_exploration', 'temperature_analysis', 'experiments', 'no_control_2'))

    for pool_folder in POOL_FOLDERS:
        gather_and_save_pool_folder(pool_folder)
