import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

import csv
import numpy as np

import filetools

from utils.temperature_tools import load_recipes
from utils.tools import read_from_json
from datasets.datasets_tools import save_list_to_csv

DATA_PATH = os.path.join(HERE_PATH, 'extracted_data')

CSV_FOLDER = os.path.join(HERE_PATH, 'time_speed_csv')
filetools.ensure_dir(CSV_FOLDER)

TIME_SPEED_FILENAME = 'time_speed.json'
PARAMS_FILENAME = 'params.json'
RUN_INFO_FILENAME=  'run_info.json'

from long_xp_tools import generate_filename_from_template

if __name__ == '__main__':

    PARAMS_TO_SCREEN = [(20, 40), (5, 10)]

    for N_FRAME_STEP, N_FRAME_WINDOW in PARAMS_TO_SCREEN:

        EXTENDED_TIME_SPEED_FILENAME = generate_filename_from_template(TIME_SPEED_FILENAME, N_FRAME_STEP, N_FRAME_WINDOW)
        files = filetools.list_files(DATA_PATH, [EXTENDED_TIME_SPEED_FILENAME])
        recipes = load_recipes()

        FEATURES_OF_INTEREST = ['average_speed']

        for feature_name in FEATURES_OF_INTEREST:
            for i, vector_recipy in enumerate(recipes):

                data_list = []

                column_names = []
                column_names.append('name')
                column_names.append('time')
                column_names.append('temperature')
                column_names.append(feature_name)
                data_list.append(column_names)

                #dep,octanol,octanoic,pentanol
                recipy = {}
                recipy['dep'] = vector_recipy[0]
                recipy['octanol'] = vector_recipy[1]
                recipy['octanoic'] = vector_recipy[2]
                recipy['pentanol'] = vector_recipy[3]

                for j, filename in enumerate(files):
                    result_folder = os.path.split(filename)[0]
                    result_folder_name = '{}_{}'.format(result_folder.split('/')[-2], result_folder.split('/')[-1])

                    params_filename = os.path.join(result_folder, PARAMS_FILENAME)
                    params = read_from_json(params_filename)

                    if recipy == params['oil_formulation']:

                        features_filename = os.path.join(result_folder, EXTENDED_TIME_SPEED_FILENAME)
                        features = read_from_json(features_filename)

                        if feature_name in features.keys():

                            run_info_filename = os.path.join(result_folder, RUN_INFO_FILENAME)
                            run_info = read_from_json(run_info_filename)

                            temperature = run_info['temperature']
                            ##
                            for time_step, feature_value in enumerate(features[feature_name]):
                                data_row = []
                                data_row.append(result_folder_name)
                                data_row.append(time_step)
                                data_row.append(temperature)
                                data_row.append(feature_value)
                                data_list.append(data_row)

                if len(data_list) > 1:

                    step_window_subfolder = '{}_{}'.format(N_FRAME_STEP, N_FRAME_WINDOW)
                    save_folder = os.path.join(CSV_FOLDER, step_window_subfolder, str(i))
                    filetools.ensure_dir(save_folder)

                    filename = os.path.join(save_folder, '{}.csv'.format(feature_name))
                    save_list_to_csv(data_list, filename)
