import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import sys
root_path = os.path.join(HERE_PATH, '..')
sys.path.append(root_path)

import csv

from constants import DATASET_FILENAME
from constants import REPEATS_FILENAME
from utils.tools import read_from_json

class LoadingError(Exception):
    pass


def format_data(raw_data):
    info = raw_data['info']
    experiments = raw_data['experiments']

    ##
    data = {}
    data['paths'] = [xp['path'] for xp in experiments]

    ##
    data['droplet_features'] = {}
    for k in experiments[0]['droplet_features'].keys():
        data['droplet_features'][k] = [xp['droplet_features'][k] for xp in experiments]

    ##
    data['droplet_composition'] = {}
    data['droplet_composition']['dep'] = []
    data['droplet_composition']['octanol'] = []
    data['droplet_composition']['octanoic'] = []
    data['droplet_composition']['pentanol'] = []
    data['droplet_composition']['vector_form'] = []
    data['droplet_composition']['ratio_vector_form'] = []
    data['droplet_composition']['json_form'] = []
    data['droplet_composition']['norm_json_form'] = []

    for xp in experiments:
        data['droplet_composition']['dep'].append(xp['params']['oil_formulation']['dep'])
        data['droplet_composition']['octanol'].append(xp['params']['oil_formulation']['octanol'])
        data['droplet_composition']['octanoic'].append(xp['params']['oil_formulation']['octanoic'])
        data['droplet_composition']['pentanol'].append(xp['params']['oil_formulation']['pentanol'])

        ## ["DEP", "1-Octanol", "Octanoic-Acid", "1-Pentanol"]
        from properties.tools import ratio_normalize
        oil_vector = [xp['params']['oil_formulation'][k] for k in ['dep', 'octanol', 'octanoic', 'pentanol']]
        ratio_oil_vector = ratio_normalize([oil_vector])[0,:].tolist()

        data['droplet_composition']['vector_form'].append(oil_vector)
        data['droplet_composition']['ratio_vector_form'].append(ratio_oil_vector)

        ##
        data['droplet_composition']['json_form'].append(xp['params']['oil_formulation'])
        norm_json_form = {}
        for i, k in enumerate(['dep', 'octanol', 'octanoic', 'pentanol']):
            norm_json_form[k] = ratio_oil_vector[i]
        data['droplet_composition']['norm_json_form'].append(norm_json_form)

    ##
    from properties.density.density_model import compute_density
    from properties.surface_tension.surface_tension_model import compute_regression_surface_tension
    from properties.viscosity.viscosity_model import compute_regression_viscosities

    data['droplet_properties'] = {}
    data['droplet_properties']['density'] = compute_density(data['droplet_composition']['ratio_vector_form']).tolist()
    data['droplet_properties']['surface_tension'] = compute_regression_surface_tension(data['droplet_composition']['ratio_vector_form']).tolist()
    data['droplet_properties']['viscosity'] = compute_regression_viscosities(data['droplet_composition']['ratio_vector_form']).tolist()

    ##
    data['xp_info'] = {}
    for k in experiments[0]['run_info'].keys():
        data['xp_info'][k] = []
        for xp in experiments:
            if xp['run_info'] is not None:
                data['xp_info'][k].append(xp['run_info'][k])
            else:
                data['xp_info'][k].append(None)

    return data


def load_dataset(dataset_filename):

    if not os.path.exists(dataset_filename):
        raise LoadingError('{} does not exist'.format(dataset_filename))

    return format_data(read_from_json(dataset_filename))


def get_dataset_basepath():
    return HERE_PATH

def forge_dataset_filename(method, seed):
    return os.path.join(get_dataset_basepath(), method, seed, DATASET_FILENAME)

def forge_dataset_filename_from_relpath(relpath):
    return os.path.join(get_dataset_basepath(), relpath, DATASET_FILENAME)

def forge_dataset_filename_from_path(path):
    return os.path.join(path, DATASET_FILENAME)

##
def format_repeats(raw_data):
    info = raw_data['info']
    experiments = raw_data['experiments']

    ##
    repeats = []
    for i_xp in range(len(experiments)):
        data = {}
        data['xp_number'] = info['xp_number'][i_xp]

        data['droplet_features'] = {}
        for k in experiments[i_xp]['original']['droplet_features'].keys():
            data['droplet_features'][k] = []
            # the first is the original
            # data['droplet_features'][k].append(experiments[i_xp]['original']['droplet_features'][k])
            # the remainings are repeats
            for i_repeat in range(len(experiments[i_xp]['repeats'])):
                data['droplet_features'][k].append(experiments[i_xp]['repeats'][i_repeat]['droplet_features'][k])

        repeats.append(data)

    return repeats


def load_repeats(dataset_filename):

    if not os.path.exists(dataset_filename):
        raise LoadingError('{} does not exist'.format(dataset_filename))

    return format_repeats(read_from_json(dataset_filename))


def forge_repeats_filename(method, seed):
    return os.path.join(HERE_PATH, method, seed, REPEATS_FILENAME)

##
def join_datasets(base_dataset, *args):
    joined_dataset = {}
    if type(base_dataset) == dict:
        for k in base_dataset.keys():
            joined_dataset[k] = join_datasets(base_dataset[k], *[arg[k] for arg in args])
        return joined_dataset
    else:
        for arg in args:
            base_dataset.extend(arg)
        return base_dataset


def sub_dataset(dataset, index):
    new_dataset = {}
    if type(dataset) == dict:
        for k in dataset.keys():
            new_dataset[k] = sub_dataset(dataset[k], index)
        return new_dataset
    else:
        return [dataset[i] for i in index]


##
def save_list_to_csv(data_list, filename):
    with open(filename, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ')
        for data in data_list:
            csvwriter.writerow(data)


def build_csv(datasets, filename):

    data_list = []

    ##
    column_names = []
    column_names.append('path')
    column_names.extend(["dep", "octanol", "octanoic", "pentanol"])
    column_names.append('temperature')
    column_names.append('humidity')
    for k, v in datasets['droplet_features'].items():
        column_names.append(k)
    for k, v in datasets['droplet_properties'].items():
        column_names.append(k)

    data_list.append(column_names)

    ##
    for i in range(len(datasets['paths'])):
        data_row = []
        data_row.append(datasets['paths'][i])
        data_row.extend(datasets['droplet_composition']['ratio_vector_form'][i])
        data_row.append(datasets['xp_info']['temperature'][i])
        data_row.append(datasets['xp_info']['humidity'][i])
        for k, v in datasets['droplet_features'].items():
            data_row.append(v[i])
        for k, v in datasets['droplet_properties'].items():
            data_row.append(v[i])

        data_list.append(data_row)

    ##
    save_list_to_csv(data_list, filename)
