import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from shapely.geometry import Point
from descartes import PolygonPatch


def save_and_close_fig(fig, filebasename, exts=['.png', '.eps', '.svg'], dpi=100, legend=None):
    for ext in exts:
        # save
        filepath = filebasename + ext
        if legend is not None:
            fig.savefig(filepath, dpi=dpi, bbox_extra_artists=(legend,), bbox_inches='tight')
        else:
            fig.savefig(filepath, dpi=dpi)

    plt.close(fig)


def plot_coverage_2D(ax, X, radius, color='#339933', alpha=1):
    X = np.atleast_2d(X)

    # only for 2D vector
    assert(X.shape[1] == 2)

    for i in range(X.shape[0]):
        px = X[i, 0]
        py = X[i, 1]
        new_point = Point(px, py).buffer(radius)
        patch = PolygonPatch(new_point, fc=color, ec=color, alpha=alpha)
        ax.add_patch(patch)
