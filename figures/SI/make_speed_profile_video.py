import os
import subprocess

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '../..')
sys.path.append(root_path)


import filetools


if __name__ == '__main__':

    from datasets.datasets_tools import load_dataset
    from datasets.datasets_tools import get_dataset_basepath

    plot_path = os.path.join(HERE_PATH, 'plot', 'speed_profile')

    xp_folders = filetools.list_folders(plot_path)
    for xp_folder in xp_folders:

        print xp_folder

        path_to_png = os.path.join(xp_folder)

        video_dir = os.path.join(plot_path)
        filetools.ensure_dir(video_dir)

        img_fname = os.path.join(path_to_png, 'time_speed_%4d.png')
        video_fname = os.path.join(video_dir, '{}.mp4'.format(os.path.split(xp_folder)[1]))
        fps = 5

        if os.path.exists(video_fname):
            os.remove(video_fname)

        bashCommand = 'avconv -r {} -i {} -b:v 1000k {}'.format(fps, img_fname, video_fname)

        print bashCommand

        p = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        p.wait()

    print 'THE END'
