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

def get_avg_XY(fname):
    positions = read_from_json(fname)

    n_frames = [len(pos) for pos in positions]
    max_frames = np.max(n_frames)

    xp_info = []
    for i, pos in enumerate(positions):
        print i

        frame_info = []
        for i_frame in range(max_frames):

            if i_frame < len(pos)  and len(pos[i_frame]) > 0:
                mean_pos = np.mean(pos[i_frame], 0)
            else:
                mean_pos = [np.nan, np.nan]

            frame_info.append(np.array(mean_pos))

        xp_info.append(np.array(frame_info))

    return np.array(xp_info)


if __name__ == '__main__':

    ALL_FILES = []
    ALL_FILES.append(os.path.join(HERE_PATH, 'random_params', '100', 'positions.json'))
    ALL_FILES.append(os.path.join(HERE_PATH, 'random_params', '101', 'positions.json'))
    ALL_FILES.append(os.path.join(HERE_PATH, 'random_params', '110', 'positions.json'))
    ALL_FILES.append(os.path.join(HERE_PATH, 'random_params', '111', 'positions.json'))
    ALL_FILES.append(os.path.join(HERE_PATH, 'random_params', '112', 'positions.json'))

    MEAN_XY = []
    for fname in ALL_FILES:
        xp_info = get_avg_XY(fname)
        MEAN_XY.append(np.nanmean(xp_info, 0).tolist())

    from utils.tools import save_to_json
    save_filename = os.path.join(HERE_PATH, 'xy.json')
    save_to_json(MEAN_XY, save_filename)
