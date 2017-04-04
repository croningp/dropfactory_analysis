import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_folder = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_folder)

import filetools

from surface_tension_model import compute_regression_surface_tension

from properties.tools import load_csv
from properties.model_plot import plot_model_vs_data
from properties.model_plot import plot_residual

from utils.plotting import save_and_close_fig

#
if __name__ == '__main__':

    csv_filename = os.path.join(HERE_PATH, 'surface_tension_data.csv')

    X, y_true = load_csv(csv_filename)

    y_pred = compute_regression_surface_tension(X)

    #
    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    #
    fig = plot_model_vs_data(y_pred, y_true, 24, 34, 'Surface Tension', '$mN.m^{-1}$', 'r')

    figbasename = os.path.join(plot_folder, 'model_vs_data')
    save_and_close_fig(fig, figbasename)

    #
    fig = plot_residual(y_pred, y_true)

    figbasename = os.path.join(plot_folder, 'residual')
    save_and_close_fig(fig, figbasename)
