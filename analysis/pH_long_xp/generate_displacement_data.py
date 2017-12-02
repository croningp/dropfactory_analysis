import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_path)

import numpy as np

import filetools

from utils.tools import read_from_json
from datasets.datasets_tools import save_list_to_csv
from utils.temperature_tools import load_recipes


DATA_PATH = os.path.join(HERE_PATH, 'extracted_data')
DISPLACEMENT_PATH = os.path.join(HERE_PATH, 'displacement_csv')


TIME_FEATURES_FILENAME = 'time_features.json'
PARAMS_FILENAME = 'params.json'
RUN_INFO_FILENAME=  'run_info.json'
DISPLACEMENT_VECTORS_FILENAME = 'displacement_vectors.json'

from long_xp_tools import generate_filename_from_template


if __name__ == '__main__':

    PARAMS_TO_SCREEN = [(20, 40), (5, 10)]

    for N_FRAME_STEP, N_FRAME_WINDOW in PARAMS_TO_SCREEN:

        EXTENDED_DISPLACEMENT_VECTORS_FILENAME = generate_filename_from_template(DISPLACEMENT_VECTORS_FILENAME, N_FRAME_STEP, N_FRAME_WINDOW)

        files = filetools.list_files(DATA_PATH, [EXTENDED_DISPLACEMENT_VECTORS_FILENAME])
        recipes = load_recipes()

        for recipy_i, vector_recipy in enumerate(recipes):

            #dep,octanol,octanoic,pentanol
            recipy = {}
            recipy['dep'] = vector_recipy[0]
            recipy['octanol'] = vector_recipy[1]
            recipy['octanoic'] = vector_recipy[2]
            recipy['pentanol'] = vector_recipy[3]

            for file_i, filename in enumerate(files):
                result_folder = os.path.split(filename)[0]

                params_filename = os.path.join(result_folder, PARAMS_FILENAME)
                params = read_from_json(params_filename)

                if recipy == params['oil_formulation']:

                    displacement_filename = os.path.join(result_folder, EXTENDED_DISPLACEMENT_VECTORS_FILENAME)
                    displacements = read_from_json(displacement_filename)

                    run_info_filename = os.path.join(result_folder, RUN_INFO_FILENAME)
                    run_info = read_from_json(run_info_filename)

                    for sequence_number, disp_info in enumerate(displacements):

                        data_list = []

                        column_names = []
                        column_names.append('time_step')
                        column_names.append('temperature')
                        column_names.append('dx')
                        column_names.append('dy')
                        column_names.append('start_x')
                        column_names.append('start_y')
                        column_names.append('end_x')
                        column_names.append('end_y')
                        data_list.append(column_names)

                        for ind in range(len(disp_info['time_step'])):

                            data_row = []
                            data_row.append(disp_info['time_step'][ind])
                            data_row.append(run_info['temperature'])
                            data_row.append(disp_info['dx'][ind])
                            data_row.append(disp_info['dy'][ind])
                            data_row.append(disp_info['start_position'][ind][0])
                            data_row.append(disp_info['start_position'][ind][1])
                            data_row.append(disp_info['end_position'][ind][0])
                            data_row.append(disp_info['end_position'][ind][1])

                            data_list.append(data_row)

                        ##
                        step_window_subfolder = '{}_{}'.format(N_FRAME_STEP, N_FRAME_WINDOW)

                        split_path = result_folder.split('/')
                        identifier = '{}_{}_T{}'.format(split_path[-2], split_path[-1], np.round(run_info['temperature'], 2))
                        save_folder = os.path.join(DISPLACEMENT_PATH, step_window_subfolder, str(recipy_i), identifier)
                        filetools.ensure_dir(save_folder)

                        save_filename = os.path.join(save_folder, '{}.csv'.format(sequence_number))
                        save_list_to_csv(data_list, save_filename)
