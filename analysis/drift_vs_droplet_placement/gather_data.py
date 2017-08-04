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

from filenaming import DROPLET_INFO_FILENAME

def read_all_xp(pool_folder):

    xptool = XPTools(pool_folder)

    data = []
    for ixp in range(xptool.info_dict['n_xp_total']):
        print '{}'.format(ixp)
        xp_folder = xptool.generate_XP_foldername(ixp)
        filename = os.path.join(xp_folder, DROPLET_INFO_FILENAME)
        droplet_info = load_video_contours_json(filename)
        frame_stats = statistics_from_video_countours(droplet_info)

        all_positions = []
        for frame_info in frame_stats:
            all_positions.append([dinfo['position'] for dinfo in frame_info])

        data.append(all_positions)

    return data

##
import filetools
from utils.tools import save_to_json

def gather_and_save_pool_folder(pool_folder):

    rel_path = os.path.relpath(pool_folder, ORKNEY_XP_FOLDER)
    save_folder = os.path.join(HERE_PATH, rel_path)
    filetools.ensure_dir(save_folder)

    save_filename = os.path.join(save_folder, 'positions.json')

    if os.path.exists(save_filename):
        print 'Skipping {} already generated'.format(rel_path)
        return

    # else do the stuff
    print 'Working on {}'.format(rel_path)
    data = read_all_xp(pool_folder)
    save_to_json(data, save_filename)


if __name__ == '__main__':

    from constants import ORKNEY_XP_FOLDER

    POOL_FOLDERS = []
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '100'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '101'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '110'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '111'))
    POOL_FOLDERS.append(os.path.join(ORKNEY_XP_FOLDER, 'random_params', '112'))

    for pool_folder in POOL_FOLDERS:
        gather_and_save_pool_folder(pool_folder)
