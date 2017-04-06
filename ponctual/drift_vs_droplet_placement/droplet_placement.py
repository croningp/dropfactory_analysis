import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '../..')
sys.path.append(root_path)

import cv2
import numpy as np

from utils.tools import read_from_json


avg_dish_info_fname = os.path.join(HERE_PATH, 'avg_dish_info.json')
avg_dish_info = read_from_json(avg_dish_info_fname)

(DISH_X, DISH_Y, DISH_R) = avg_dish_info['dish_circle']

DISH_RADIUS_MM = 14.0
PIXEL_TO_MM = DISH_RADIUS_MM/DISH_R
MM_TO_PIXEL = 1.0 / PIXEL_TO_MM


ANGLE = -3.*np.pi/4.
ROTATION_MATRIX = np.matrix([[np.cos(ANGLE), -np.sin(ANGLE)], [np.sin(ANGLE), np.cos(ANGLE)]])
SHIFT_PIXEL = [DISH_X, DISH_Y]

def dish_mm_to_camera_pixel(xy_dish_mm):

    position = np.matrix(xy_dish_mm)
    rotated = np.array(position*ROTATION_MATRIX)
    rotated_pixel = rotated * MM_TO_PIXEL
    translated_pixel = rotated_pixel + SHIFT_PIXEL
    return translated_pixel

OLD_PLACEMENT_MM = [(5,0), (-5,0), (0,5), (0,-5)]
NEW_PLACEMENT_MM = [(0,0), (-5,0), (2.5,4.33), (2.5,-4.33)]

OLD_PLACEMENT_PIXEL = [dish_mm_to_camera_pixel(xy).tolist()[0] for xy in OLD_PLACEMENT_MM]
NEW_PLACEMENT_PIXEL = [dish_mm_to_camera_pixel(xy).tolist()[0] for xy in NEW_PLACEMENT_MM]

if __name__ == '__main__':


    video_filename = os.path.join(HERE_PATH, 'media', 'video.avi')

    video_capture = cv2.VideoCapture(video_filename)
    ret, frame = video_capture.read()
    video_capture.release()

    import matplotlib.pyplot as plt
    from utils.plotting import save_and_close_fig

    shift_text = 20

    fig = plt.figure(figsize=(16, 8))

    plt.subplot(1, 2, 1)
    plt.imshow(frame)

    for i, old_pos in enumerate(OLD_PLACEMENT_PIXEL):
        plt.scatter(old_pos[0], old_pos[1], 200, 'k')
        plt.text(old_pos[0]+shift_text, old_pos[1]+shift_text, '{}'.format(i+1), fontsize=30)

    ##
    plt.subplot(1, 2, 2)
    plt.imshow(frame)

    for i, old_pos in enumerate(NEW_PLACEMENT_PIXEL):
        plt.scatter(old_pos[0], old_pos[1], 200, 'k')
        plt.text(old_pos[0]+shift_text, old_pos[1]+shift_text, '{}'.format(i+1), fontsize=30)

    plt_fname = os.path.join(HERE_PATH, 'plot', 'placement')
    save_and_close_fig(fig, plt_fname)
