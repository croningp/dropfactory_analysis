import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

import numpy as np
from shutil import copyfile

import filetools

from chemobot_tools.droplet_tracking.droplet_feature import load_video_contours_json
from chemobot_tools.droplet_tracking.droplet_feature import load_dish_info
from chemobot_tools.droplet_tracking.droplet_feature import compute_droplet_features
from chemobot_tools.droplet_tracking.droplet_feature import aggregate_droplet_info

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
DISPLACEMENT_VECTORS_FILENAME = 'displacement_vectors.json'

TMP_DROPLET_INFO_FILE = os.path.join(TMP_PATH, 'tmp_droplet_info.json')
TMP_DISH_INFO_FILENAME = os.path.join(TMP_PATH, 'tmp_dish_info.json')
TMP_FEATURE_FILE = os.path.join(TMP_PATH, 'tmp_droplet_features.json')
SAMPLE_VIDEO = os.path.join(HERE_PATH, 'sample_video.avi')



def handle_features_xp_folder(xp_folder):

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


def handle_direction_vectors_xp_folder(xp_folder):

    print 'Working on {}'.format(xp_folder)

    time_displacement_vectors_filename = xp_folder.replace(LONG_XP_PATH, '')
    time_displacement_vectors_filename = os.path.join(DATA_PATH, time_displacement_vectors_filename, DISPLACEMENT_VECTORS_FILENAME)

    if os.path.exists(time_displacement_vectors_filename):
        print 'Skipping, already processed'
        return

    ##
    droplet_info_filename = os.path.join(xp_folder, DROPLET_INFO_FILENAME)
    droplet_info = read_from_json(droplet_info_filename)
    save_to_json(droplet_info, TMP_DROPLET_INFO_FILE)

    dish_info_filename = os.path.join(xp_folder, DISH_INFO_FILENAME)
    dish_info = read_from_json(dish_info_filename)
    save_to_json(dish_info, TMP_DISH_INFO_FILENAME)

    dish_diameter_pixel = 2 * dish_info['dish_circle'][2]
    dish_diameter_mm = 28
    pixel_to_mm = dish_diameter_mm / np.float(dish_diameter_pixel)

    agregate_config = {
        'dish_info_filename': TMP_DISH_INFO_FILENAME,
        'droplet_info_filename': TMP_DROPLET_INFO_FILE,
        'max_distance_tracking': 100,
        'min_sequence_length': 20,
        'join_min_frame_dist': 1,
        'join_max_frame_dist': 10,
        'min_droplet_radius': 5
    }

    ## new analysis for position extraction
    dish_info, droplet_info, droplets_statistics, high_level_frame_stats, droplets_ids, grouped_stats = aggregate_droplet_info(**agregate_config)

    n_frame = len(droplet_info)

    all_displacements = []
    for i , droplet_stats in enumerate(grouped_stats):

        print 'Droplet sequence {} / {}'.format(i, len(grouped_stats))

        displacement_info = {}
        displacement_info['time_step'] = []
        displacement_info['dx'] = []
        displacement_info['dy'] = []
        displacement_info['start_position'] = []
        displacement_info['end_position'] = []

        start_index = 0
        end_index = start_index + N_FRAME_WINDOW
        time_step = 0

        while True:
            if start_index in droplet_stats['frame_id']:
                if end_index in droplet_stats['frame_id']:

                    start_array_index = droplet_stats['frame_id'].index(start_index)
                    end_array_index = droplet_stats['frame_id'].index(end_index)

                    start_position = droplet_stats['position'][start_array_index]
                    end_position = droplet_stats['position'][end_array_index]

                    start_position = [e * pixel_to_mm for e in start_position]
                    end_position = [e * pixel_to_mm for e in end_position]

                    displacement_info['time_step'].append(time_step)
                    displacement_info['dx'].append(end_position[0] - start_position[0])
                    displacement_info['dy'].append(end_position[1] - start_position[1])
                    displacement_info['start_position'].append(start_position)
                    displacement_info['end_position'].append(end_position)
            #
            start_index += N_FRAME_STEP
            end_index = start_index + N_FRAME_WINDOW
            time_step = time_step + 1
            if end_index >= n_frame:
                break

        all_displacements.append(displacement_info)

    ## save
    filetools.ensure_dir(os.path.split(time_displacement_vectors_filename)[0])
    save_to_json(all_displacements, time_displacement_vectors_filename)


def copy_info(xp_folder):

    remote_params_filename = os.path.join(xp_folder, PARAMS_FILENAME)
    if os.path.exists(remote_params_filename):
        local_params_filename = xp_folder.replace(LONG_XP_PATH, '')
        local_params_filename = os.path.join(DATA_PATH, local_params_filename, PARAMS_FILENAME)
        if not os.path.exists(local_params_filename):
            copyfile(remote_params_filename, local_params_filename)

    remote_run_info_filename = os.path.join(xp_folder, RUN_INFO_FILENAME)
    if os.path.exists(remote_run_info_filename):
        local_run_info_filename = xp_folder.replace(LONG_XP_PATH, '')
        local_run_info_filename = os.path.join(DATA_PATH, local_run_info_filename, RUN_INFO_FILENAME)
        if not os.path.exists(local_run_info_filename):
            copyfile(remote_run_info_filename, local_run_info_filename)



if __name__ == '__main__':

    LONG_XP_PATH = '/home/group/orkney1/Chemobot/dropfactory_exploration/realworld_experiments/manual_exploration/temperature_long_xp/experiments/'

    files = filetools.list_files(LONG_XP_PATH, [DROPLET_INFO_FILENAME])

    for filename in files:
        xp_folder = os.path.split(filename)[0]
        handle_features_xp_folder(xp_folder)

    for filename in files:
        xp_folder = os.path.split(filename)[0]
        handle_direction_vectors_xp_folder(xp_folder)

    for filename in files:
        xp_folder = os.path.split(filename)[0]
        copy_info(xp_folder)
