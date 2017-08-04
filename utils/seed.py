import random
import numpy as np


def set_seed(seed, verbose=True):
    if verbose:
        print 'Setting seed to {}'.format(seed)
    random.seed(seed)
    np.random.seed(seed)
