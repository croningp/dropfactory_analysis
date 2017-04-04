import os

# this get our current location in the file system
import inspect
HERE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# adding parent directory to path, so we can access the utils easily
import sys
root_folder = os.path.join(HERE_PATH, '..', '..')
sys.path.append(root_folder)

import filetools

from viscosity_model import compute_formula_viscosities
from viscosity_model import compute_regression_viscosities

from properties.tools import load_csv
from properties.model_plot import plot_model_vs_data
from properties.model_plot import plot_residual

from utils.plotting import save_and_close_fig

#
import matplotlib
import matplotlib.pyplot as plt
import seaborn

# design figure
fontsize = 26
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)
matplotlib.rcParams.update({'font.size': fontsize})


if __name__ == '__main__':

    csv_filename = os.path.join(HERE_PATH, 'viscosities_data.csv')

    X, y_true = load_csv(csv_filename)

    y_pred_formula = compute_formula_viscosities(X)
    y_pred_regressor = compute_regression_viscosities(X)

    #
    plot_folder = os.path.join(HERE_PATH, 'plot')
    filetools.ensure_dir(plot_folder)

    min_value = 3
    max_value = 12
    property_name = 'Viscosity'
    units = '$mPa.s$'

    #
    fig = plot_model_vs_data(y_pred_formula, y_true, min_value, max_value, property_name)

    figbasename = os.path.join(plot_folder, 'formula_vs_data')
    save_and_close_fig(fig, figbasename, exts=['.png'])

    #
    fig = plot_residual(y_pred_formula, y_true)

    figbasename = os.path.join(plot_folder, 'formula_residual')
    save_and_close_fig(fig, figbasename, exts=['.png'])

    #
    fig = plot_model_vs_data(y_pred_regressor, y_true, min_value, max_value, property_name)

    figbasename = os.path.join(plot_folder, 'regressor_vs_data')
    save_and_close_fig(fig, figbasename, exts=['.png'])

    #
    fig = plot_residual(y_pred_regressor, y_true)

    figbasename = os.path.join(plot_folder, 'regressor_residual')
    save_and_close_fig(fig, figbasename, exts=['.png'])

    #
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, aspect='equal')
    hdl1 = ax.scatter(y_pred_formula, y_true, 50, c = 'b')
    hdl2 = ax.scatter(y_pred_regressor, y_true, 50, c = 'r')
    ax.plot([min_value, max_value], [min_value, max_value], 'k--')
    ax.set_xlim([min_value, max_value])
    ax.set_ylim([min_value, max_value])
    x0,x1 = ax.get_xlim()
    y0,y1 = ax.get_ylim()
    ax.set_aspect(abs(x1-x0)/abs(y1-y0))
    plt.xlabel('{} Predicted / {}'.format(property_name, units), fontsize=fontsize)
    plt.ylabel('{} Measured / {}'.format(property_name, units), fontsize=fontsize)
    plt.legend([hdl1, hdl2], ['Formula', 'Regressor'], fontsize=fontsize, loc=2)
    plt.tight_layout()

    figbasename = os.path.join(plot_folder, 'method_comparison')
    save_and_close_fig(fig, figbasename, exts=['.png'])
