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

    dataset_path = get_dataset_basepath()
    plot_path = os.path.join(HERE_PATH, 'plot', 'scatter_interval_per_run')

    data_files = filetools.list_files(dataset_path, 'data.json')
    for data_file in data_files:
        print '###'
        print '###'
        print data_file
        print '###'
        print '###'
        data = load_dataset(data_file)
        if len(data['paths']) == 1000:
            plot_folder = os.path.split(data_file)[0].replace(dataset_path, plot_path)

            path_to_png = os.path.join(plot_folder, 'png')

            video_dir = os.path.join(plot_folder, 'video')
            filetools.ensure_dir(video_dir)

            img_fname = os.path.join(path_to_png, 'exploration_raw_%4d.png')
            video_fname = os.path.join(video_dir, 'exploration_raw_video.mp4')
            fps = 20

            if os.path.exists(video_fname):
                os.remove(video_fname)

            bashCommand = 'avconv -r {} -i {} -b:v 1000k {}'.format(fps, img_fname, video_fname)

            print bashCommand

            p = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            p.wait()

    print 'THE END'
