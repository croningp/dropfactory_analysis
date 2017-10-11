import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

from shutil import copyfile

import filetools

from chemobot_tools.droplet_tracking.droplet_feature import load_video_contours_json
from chemobot_tools.droplet_tracking.droplet_feature import load_dish_info
from chemobot_tools.droplet_tracking.droplet_feature import compute_droplet_features

from utils.tools import save_to_json
from utils.tools import read_from_json

DATA_PATH = os.path.join(HERE_PATH, 'extracted_data')
filetools.ensure_dir(DATA_PATH)
TMP_PATH = os.path.join(HERE_PATH, 'tmp')
filetools.ensure_dir(TMP_PATH)

N_FRAME_WINDOW = 40  # 20fps
N_FRAME_STEP = 20

DROPLET_INFO_FILENAME = 'droplet_info.json'
DISH_INFO_FILENAME = 'dish_info.json'
VIDEO_FILENAME = 'video.avi'
TIME_FEATURES_FILENAME = 'time_features.json'
PARAMS_FILENAME = 'params.json'
RUN_INFO_FILENAME=  'run_info.json'

TMP_DROPLET_INFO_FILE = os.path.join(TMP_PATH, 'tmp_droplet_info.json')
TMP_DISH_INFO_FILENAME = os.path.join(TMP_PATH, 'tmp_dish_info.json')
TMP_FEATURE_FILE = os.path.join(TMP_PATH, 'tmp_droplet_features.json')
SAMPLE_VIDEO = os.path.join(HERE_PATH, 'sample_video.avi')

def handle_xp_folder(xp_folder):

    print 'Working on {}'.format(xp_folder)

    time_features_filename = xp_folder.replace(LONG_XP_PATH, '')
    time_features_filename = os.path.join(DATA_PATH, time_features_filename, TIME_FEATURES_FILENAME)

    if os.path.exists(time_features_filename):
        print 'Skipping, already processed'
        return

    ##
    droplet_info_filename = os.path.join(xp_folder, DROPLET_INFO_FILENAME)
    droplet_info = read_from_json(droplet_info_filename)

    dish_info_filename = os.path.join(xp_folder, DISH_INFO_FILENAME)
    dish_info = read_from_json(dish_info_filename)
    save_to_json(dish_info, TMP_DISH_INFO_FILENAME)


    features_config = {
        'dish_info_filename': TMP_DISH_INFO_FILENAME,
        'droplet_info_filename': TMP_DROPLET_INFO_FILE,
        'max_distance_tracking': 100,
        'min_sequence_length': 20,
        'join_min_frame_dist': 1,
        'join_max_frame_dist': 10,
        'min_droplet_radius': 5,
        'dish_diameter_mm': 28,
        'frame_per_seconds': 20,
        'features_out': TMP_FEATURE_FILE,
        'video_in': SAMPLE_VIDEO,  # just needed to compute coverage to get frame size
        'no_video': True
    }

    n_frame = len(droplet_info)

    start_index = 0
    end_index = start_index + N_FRAME_WINDOW

    time_features = None
    while True:
        print '{}->{} / {}'.format(start_index, end_index, n_frame)

        save_to_json(droplet_info[start_index:end_index], TMP_DROPLET_INFO_FILE)
        compute_droplet_features(**features_config)
        droplet_features = read_from_json(TMP_FEATURE_FILE)

        if time_features is None:
            time_features = {}
            for k in droplet_features.keys():
                time_features[k] = [droplet_features[k]]
        else:
            for k in droplet_features.keys():
                time_features[k].extend([droplet_features[k]])

        start_index += N_FRAME_STEP
        end_index = start_index + N_FRAME_WINDOW
        if end_index >= n_frame:
            break

    ## save
    filetools.ensure_dir(os.path.split(time_features_filename)[0])
    save_to_json(time_features, time_features_filename)


def copy_info(xp_folder):

    remote_params_filename = os.path.join(xp_folder, PARAMS_FILENAME)
    local_params_filename = xp_folder.replace(LONG_XP_PATH, '')
    local_params_filename = os.path.join(DATA_PATH, local_params_filename, PARAMS_FILENAME)
    if not os.path.exists(local_params_filename):
        copyfile(remote_params_filename, local_params_filename)

    remote_run_info_filename = os.path.join(xp_folder, RUN_INFO_FILENAME)
    local_run_info_filename = xp_folder.replace(LONG_XP_PATH, '')
    local_run_info_filename = os.path.join(DATA_PATH, local_run_info_filename, RUN_INFO_FILENAME)
    if not os.path.exists(local_run_info_filename):
        copyfile(remote_run_info_filename, local_run_info_filename)



if __name__ == '__main__':

    LONG_XP_PATH = '/home/group/orkney1/Chemobot/dropfactory_exploration/realworld_experiments/manual_exploration/temperature_long_xp/experiments/'

    files = filetools.list_files(LONG_XP_PATH, [DROPLET_INFO_FILENAME])

    for filename in files:
        xp_folder = os.path.split(filename)[0]
        handle_xp_folder(xp_folder)
        copy_info(xp_folder)
