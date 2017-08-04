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

#
from xp_utils import XPTools

from chemobot_tools.droplet_tracking.droplet_feature import load_video_contours_json
from chemobot_tools.droplet_tracking.droplet_feature import statistics_from_video_countours

from filenaming import DISH_INFO_FILENAME

import numpy as np

def read_all_xp(pool_folder):

    xptool = XPTools(pool_folder)

    dish_circles = []
    arena_circles = []
    for ixp in range(xptool.info_dict['n_xp_total']):
        dish_info = xptool.get_json_content_from_xp_number_and_filename(0, DISH_INFO_FILENAME)

        dish_circles.append(dish_info['dish_circle'])
        arena_circles.append(dish_info['arena_circle'])

    return np.mean(dish_circles, 0), np.mean(arena_circles, 0)

if __name__ == '__main__':

    from constants import ORKNEY_XP_FOLDER

    POOL_FOLDERS = []
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '100'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '101'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '110'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '111'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '112'))

    dish_circles = []
    arena_circles = []
    for pool_folder in POOL_FOLDERS:
        dish_circle, arena_circle = read_all_xp(pool_folder)
        dish_circles.append(dish_circle)
        arena_circles.append(arena_circle)

    ##
    AVG_DISH = {}
    AVG_DISH['dish_circle'] = np.mean(dish_circles, 0).tolist()
    AVG_DISH['arena_circle'] = np.mean(arena_circles, 0).tolist()

    from utils.tools import save_to_json
    save_filename = os.path.join(HERE_PATH, 'avg_dish_info.json')
    save_to_json(AVG_DISH, save_filename)
