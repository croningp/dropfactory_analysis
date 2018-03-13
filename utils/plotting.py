import numpy as np
from scipy import stats

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from shapely.geometry import Point
from descartes import PolygonPatch

from matplotlib.collections import LineCollection


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


def plot_kde(ax, kde_data, bounds = [0, 1, 0, 1], resolution=100j, bandwidth=None, cmap=plt.cm.gist_earth_r):

    XMIN = bounds[0]
    XMAX = bounds[1]
    YMIN = bounds[2]
    YMAX = bounds[3]

    X, Y = np.mgrid[XMIN:XMAX:resolution, YMIN:YMAX:resolution]
    POSITIONS = np.vstack([X.ravel(), Y.ravel()])

    if bandwidth is not None:
        kernel = stats.gaussian_kde(kde_data, bw_method=bandwidth)
    else:
        kernel = stats.gaussian_kde(kde_data)

    Z = np.reshape(kernel(POSITIONS).T, X.shape)

    cax = ax.imshow(np.rot90(Z), cmap=cmap, extent=[XMIN, XMAX, YMIN, YMAX])

    return cax


def plot_convex_hull(hull):
    for i in range(len(hull.vertices)):
        x = [hull.points[hull.vertices[i-1],0], hull.points[hull.vertices[i],0]]
        y = [hull.points[hull.vertices[i-1],1], hull.points[hull.vertices[i], 1]]
        plt.plot(x, y, 'r--', lw=2)



def plot_concave_hull(concave_hull, edge_points, X):

    points = [Point(x) for x in X]

    #print concave_hull
    lines = LineCollection(edge_points)
    plt.gca().add_collection(lines)
    delaunay_points = np.array([point.coords[0]
                                for point in points])
    plt.plot(delaunay_points[:,0], delaunay_points[:,1],
            'o', hold=1, color='#f16824')
