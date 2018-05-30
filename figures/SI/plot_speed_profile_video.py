import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '../..')
sys.path.append(root_path)

from utils.tools import read_from_json

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 34
matplotlib.rc('xtick', labelsize=30)
matplotlib.rc('ytick', labelsize=30)
matplotlib.rcParams.update({'font.size': fontsize})

from utils.plotting import save_and_close_fig

X_FEATURE_LABEL = 'Time / $s$'
Y_FEATURE_LABEL = 'Droplet Speed / $mm.s^{-1}$'


def plot_experiment(data, color, timestep):

    fig  = plt.figure(figsize=(12,9))
    with sns.axes_style("ticks"):
        ax = plt.subplot(111)

    x = range(len(data['average_speed']))
    y = data['average_speed']

    plt.scatter(x, y, 50, c=color)
    plt.plot([timestep, timestep], [0, 25], 'g', linewidth=3)

    plt.xlim(0, 900)
    plt.xticks(range(0, 1000, 100))

    plt.ylim(0, 25)
    plt.yticks(range(0, 30, 5))

    plt.xlabel(X_FEATURE_LABEL)
    plt.ylabel(Y_FEATURE_LABEL)

    plt.tight_layout()

    return fig

if __name__ == '__main__':

    import filetools

    experiment_folders = []
    experiment_folders.append(os.path.join(root_path, 'analysis/temperature_long_xp/extracted_data/AC_22/00019'))
    experiment_folders.append(os.path.join(root_path, 'analysis/temperature_long_xp/extracted_data/no_control_1/00019'))
    experiment_folders.append(os.path.join(root_path, 'analysis/temperature_long_xp/extracted_data/AC_28.0/00031'))

    color_palette = sns.color_palette("Paired", 10)

    colors = []
    colors.append(color_palette[1])
    colors.append(color_palette[7])
    colors.append(color_palette[5])

    time_speed_filename = 'time_speed_20_40.json'
    run_info_filename = 'run_info.json'

    fps = 1

    for experiment_folder, color in zip(experiment_folders, colors):

        print experiment_folder

        time_speed_data = read_from_json(os.path.join(experiment_folder, time_speed_filename))
        run_info_data = read_from_json(os.path.join(experiment_folder, run_info_filename))

        plot_folder = os.path.join(HERE_PATH, 'plot', 'speed_profile', str(run_info_data['temperature']))
        filetools.ensure_dir(plot_folder)

        frame_id = 0
        for timestep in range(len(time_speed_data['average_speed'])):

            print timestep

            for _ in range(fps):
                fig = plot_experiment(time_speed_data, color, timestep)
                plot_filebasename = os.path.join(plot_folder, 'time_speed_{:04d}'.format(frame_id))
                save_and_close_fig(fig, plot_filebasename, exts=['.png'], dpi=100)
                frame_id += 1
