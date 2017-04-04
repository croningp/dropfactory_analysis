import matplotlib
import matplotlib.pyplot as plt
import seaborn

# design figure
fontsize = 26
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)
matplotlib.rcParams.update({'font.size': fontsize})


def plot_model_vs_data(y_pred, y_true, min_value, max_value, property_name, units='', color='b', figsize=(10, 10)):

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, aspect='equal')
    ax.plot([min_value, max_value], [min_value, max_value], 'k--')
    ax.scatter(y_pred, y_true, 50, c=color)
    ax.set_xlim([min_value, max_value])
    ax.set_ylim([min_value, max_value])
    x0,x1 = ax.get_xlim()
    y0,y1 = ax.get_ylim()
    ax.set_aspect(abs(x1-x0)/abs(y1-y0))
    plt.xlabel('{} Predicted / {}'.format(property_name, units), fontsize=fontsize)
    plt.ylabel('{} Measured / {}'.format(property_name, units), fontsize=fontsize)
    plt.tight_layout()

    return fig


def plot_residual(y_pred, y_true, figsize=(12, 8)):

    fig = plt.figure(figsize=figsize)
    plt.plot(y_pred-y_true)
    plt.xlabel('Measurement Number', fontsize=fontsize)
    plt.ylabel('Regression Error', fontsize=fontsize)
    plt.tight_layout()

    return fig
