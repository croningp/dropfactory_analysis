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

from utils.tools import save_to_json

from chemobot_tools.droplet_tracking.tools import get_median_dish_from_video
from chemobot_tools.droplet_tracking.tools import create_dish_arena
from chemobot_tools.droplet_tracking.tools import binarize_frame

import cv2
WAITKEY_TIME = 1

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# design figure
fontsize = 30
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rcParams.update({'font.size': fontsize})


DISH_CONFIG = {
    'minDist': np.inf,
    'hough_config': {},
    'dish_center': None,
    'dish_radius': None
}

DISH_FRAME_SPACING = 1000
ARENA_RATIO = 0.8

GRAY_THRESHOLD = 70


def draw_frame_detection(frame, dish_circle, arena_circle):
    # draw the dish circle
    plot_frame = frame.copy()
    cv2.circle(plot_frame, (dish_circle[0], dish_circle[1]), int(dish_circle[2]), (0, 0, 255), 3)
    cv2.circle(plot_frame, (arena_circle[0], arena_circle[1]), int(arena_circle[2]), (255, 0, 0), 3)
    return plot_frame


def compute_mean_hue(videofilename):

    dish_circle, dish_mask = get_median_dish_from_video(video_filename, DISH_CONFIG, frame_spacing=DISH_FRAME_SPACING)
    arena_circle, arena_mask = create_dish_arena(dish_circle, dish_mask, ARENA_RATIO)

    # open video to play with frames
    video_capture = cv2.VideoCapture(video_filename)
    ret, frame = video_capture.read()

    mean_hue = []
    frame_count = 0
    while ret:
        frame_count += 1

        if frame_count % 100 == 0:
            print frame_count

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # lower_blue = np.array([0,0,50])
        # upper_blue = np.array([255,255,255])
        # droplet_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        droplet_mask = binarize_frame(frame, GRAY_THRESHOLD)
        droplet_mask = cv2.bitwise_not(droplet_mask)

        arena_mask_bool = np.array(arena_mask, dtype='bool')

        mask = cv2.bitwise_and(droplet_mask, arena_mask)

        to_process_frame = hsv_frame[:,:,0][arena_mask_bool].ravel()
        mean_hue.append(np.mean(to_process_frame))

        # if frame_count % 60000 == 0:
        #     print frame_count
        #     plt.clf()
        #     for i in range(3):
        #         hist_data, bins = np.histogram(hsv_frame[:,:,i][arena_mask_bool], np.arange(256))
        #         positions = bins[:-1] + np.diff(bins)/2.0
        #         plt.plot(positions, hist_data)
        #     hist_data, bins = np.histogram(gray_frame[arena_mask_bool], np.arange(256))
        #     positions = bins[:-1] + np.diff(bins)/2.0
        #     plt.plot(positions, hist_data)
        #     for i in range(3):
        #         hist_data, bins = np.histogram(frame[:,:,i][arena_mask_bool], np.arange(256))
        #         positions = bins[:-1] + np.diff(bins)/2.0
        #         plt.plot(positions, hist_data)
        #     plt.draw()
        #     raw_input()

        # cv2.imshow("frame", frame)
        # # plot_frame = draw_frame_detection(mask, dish_circle, arena_circle)
        # cv2.imshow("extract", mask)
        # cv2.waitKey(WAITKEY_TIME)

        # next frame
        ret, frame = video_capture.read()

    video_capture.release()

    return mean_hue



if __name__ == '__main__':

    import filetools

    XP_PATH = '/home/group/orkney1/Chemobot/dropfactory_exploration/realworld_experiments/manual_exploration/dye_release_xp/experiments'

    DATA_PATH = os.path.join(HERE_PATH, 'data')

    video_files = filetools.list_files(XP_PATH, ['video.avi'])

    for video_filename in video_files:
        print 'Working on {}'.format(video_filename)

        xp_folder = os.path.split(video_filename)[0]
        save_folder = xp_folder.replace(XP_PATH, DATA_PATH)
        save_filename = os.path.join(save_folder, 'mean_hue.json')

        mean_hue = compute_mean_hue(video_filename)

        results = {}
        results['mean_hue'] = mean_hue

        filetools.ensure_dir(save_folder)
        save_to_json(results, save_filename)


    # video_filename = '/home/group/orkney1/Chemobot/dropfactory_exploration/realworld_experiments/manual_exploration/dye_release_xp/experiments/AC_19.0_LJP5-22-Ey/00000/video.avi'
    #
    # mean_hue_cold = compute_mean_hue(video_filename)
    #
    # video_filename = '/home/group/orkney1/Chemobot/dropfactory_exploration/realworld_experiments/manual_exploration/dye_release_xp/experiments/AC_28_LJP5-22-Ey/00000/video.avi'
    #
    # mean_hue_hot = compute_mean_hue(video_filename)
    #
    # plt.plot(mean_hue_cold, 'b')
    # plt.plot(mean_hue_hot, 'r')
