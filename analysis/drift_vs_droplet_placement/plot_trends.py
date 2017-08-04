import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_path = os.path.join(HERE_PATH, '../..')
sys.path.append(root_path)

from constants import DROPFACTORY_UTILS_PATH
sys.path.append(DROPFACTORY_UTILS_PATH)

from xp_utils import XPTools

from utils.tools import read_from_json

import numpy as np


def circle_point(center, radius, n_angle_step=360):
    # theta goes from 0 to 2pi
    theta = np.linspace(0, 2*np.pi, n_angle_step)
    x = radius*np.cos(theta) + center[0]
    y = radius*np.sin(theta) + center[1]

    return x, y


if __name__ == '__main__':

    avg_dish_info_fname = os.path.join(HERE_PATH, 'avg_dish_info.json')
    avg_dish_info = read_from_json(avg_dish_info_fname)

    (dish_x, dish_y, dish_r) = avg_dish_info['dish_circle']
    dish_px, dish_py = circle_point((dish_x, dish_y), dish_r)

    (arena_x, arena_y, arena_r) = avg_dish_info['arena_circle']
    arena_px, arena_py = circle_point((arena_x, arena_y), arena_r)

    ##
    DISH_RADIUS_MM = 14.0
    PIXEL_TO_MM = DISH_RADIUS_MM/dish_r
    MM_TO_PIXEL = 1.0 / PIXEL_TO_MM

    ##
    fname = os.path.join(HERE_PATH, 'xy.json')
    mean_xy = np.array(read_from_json(fname))

    ##
    import matplotlib.pyplot as plt
    from utils.plotting import save_and_close_fig
    import filetools

    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    ##
    from droplet_placement import OLD_PLACEMENT_PIXEL
    from droplet_placement import NEW_PLACEMENT_PIXEL



    ##
    fig = plt.figure(figsize=(16,8))
    shift_text = 7

    ax=plt.subplot(1,2,1)
    ax.set_aspect('equal')
    plt.plot(dish_px, dish_py, 'b')
    plt.plot(arena_px, arena_py, 'r')

    plt.plot(mean_xy[0][:,0], mean_xy[0][:,1], 'b')
    plt.plot(mean_xy[1][:,0], mean_xy[1][:,1], 'g')

    plt.scatter(mean_xy[0][0,0], mean_xy[0][0,1], 200, c='k', marker='+')
    plt.scatter(mean_xy[1][0,0], mean_xy[1][0,1], 200, c='k', marker='+')

    for i, old_pos in enumerate(OLD_PLACEMENT_PIXEL):
        plt.scatter(old_pos[0], old_pos[1], 50, 'k')
        plt.text(old_pos[0]+shift_text, old_pos[1]+shift_text, '{}'.format(i+1), fontsize=10)

    plt.xlim([0, 640])
    plt.ylim([0, 480])
    
    plt.gca().invert_yaxis()
    plt.title('OLD PLACEMENT')

    ax=plt.subplot(1,2,2)
    ax.set_aspect('equal')
    plt.plot(dish_px, dish_py, 'b')
    plt.plot(arena_px, arena_py, 'r')

    plt.plot(mean_xy[2][:,0], mean_xy[2][:,1])
    plt.plot(mean_xy[3][:,0], mean_xy[3][:,1])
    plt.plot(mean_xy[4][:,0], mean_xy[4][:,1])

    plt.scatter(mean_xy[2][0,0], mean_xy[2][0,1], 200, c='k', marker='+')
    plt.scatter(mean_xy[3][0,0], mean_xy[3][0,1], 200, c='k', marker='+')
    plt.scatter(mean_xy[4][0,0], mean_xy[4][0,1], 200, c='k', marker='+')

    for i, old_pos in enumerate(NEW_PLACEMENT_PIXEL):
        plt.scatter(old_pos[0], old_pos[1], 50, 'k')
        plt.text(old_pos[0]+shift_text, old_pos[1]+shift_text, '{}'.format(i+1), fontsize=10)

    plt.xlim([0, 640])
    plt.ylim([0, 480])

    plt.gca().invert_yaxis()
    plt.title('NEW PLACEMENT')

    plot_filename = os.path.join(plot_folder, 'zoomed_out')
    save_and_close_fig(fig, plot_filename)

    ##
    ##
    ##
    ##
    ##
    ##
    fig = plt.figure(figsize=(16,8))
    shift_text = 3
    zoom_window = 80

    ax=plt.subplot(1,2,1)
    ax.set_aspect('equal')

    plt.plot([dish_x, dish_x], [0, 500], 'k')
    plt.plot([0, 500], [dish_y, dish_y], 'k')

    plt.plot(mean_xy[0][:,0], mean_xy[0][:,1], 'b')
    plt.plot(mean_xy[1][:,0], mean_xy[1][:,1], 'g')

    plt.scatter(mean_xy[0][0,0], mean_xy[0][0,1], 200, c='k', marker='+')
    plt.scatter(mean_xy[1][0,0], mean_xy[1][0,1], 200, c='k', marker='+')

    for i, old_pos in enumerate(OLD_PLACEMENT_PIXEL):
        plt.scatter(old_pos[0], old_pos[1], 200, 'k')
        plt.text(old_pos[0]+shift_text, old_pos[1]+shift_text, '{}'.format(i+1), fontsize=20)

    plt.xlim([dish_x-zoom_window, dish_x+zoom_window])
    plt.ylim([dish_y-zoom_window, dish_y+zoom_window])

    plt.gca().invert_yaxis()
    plt.title('OLD PLACEMENT')

    ax=plt.subplot(1,2,2)
    ax.set_aspect('equal')

    plt.plot([dish_x, dish_x], [0, 500], 'k')
    plt.plot([0, 500], [dish_y, dish_y], 'k')

    plt.plot(mean_xy[2][:,0], mean_xy[2][:,1])
    plt.plot(mean_xy[3][:,0], mean_xy[3][:,1])
    plt.plot(mean_xy[4][:,0], mean_xy[4][:,1])

    plt.scatter(mean_xy[2][0,0], mean_xy[2][0,1], 200, c='k', marker='+')
    plt.scatter(mean_xy[3][0,0], mean_xy[3][0,1], 200, c='k', marker='+')
    plt.scatter(mean_xy[4][0,0], mean_xy[4][0,1], 200, c='k', marker='+')

    for i, old_pos in enumerate(NEW_PLACEMENT_PIXEL):
        plt.scatter(old_pos[0], old_pos[1], 200, 'k')
        plt.text(old_pos[0]+shift_text, old_pos[1]+shift_text, '{}'.format(i+1), fontsize=20)

    plt.xlim([dish_x-zoom_window, dish_x+zoom_window])
    plt.ylim([dish_y-zoom_window, dish_y+zoom_window])


    plt.gca().invert_yaxis()
    plt.title('NEW PLACEMENT')

    plot_filename = os.path.join(plot_folder, 'zoomed_in')
    save_and_close_fig(fig, plot_filename)
