import math
import numpy as np

from scipy.spatial import ConvexHull
from scipy.spatial import Delaunay

from shapely.ops import cascaded_union, polygonize
from shapely.geometry import Point, MultiPoint, MultiLineString

def compute_explored_volume(X, radius):
    # only for 2D vector
    assert(X.shape[1] == 2)

    volumes = []

    for i in range(X.shape[0]):
        px = X[i, 0]
        py = X[i, 1]
        new_point = Point(px, py).buffer(radius)
        if i == 0:
            patch = new_point
        else:
            patch = patch.union(new_point)
        volumes.append(patch.area)

    return volumes


def compute_volume_convex_hull(X, last_only=False):

    if last_only:
        hull = ConvexHull(X)
        return hull.volume, hull

    else:
        volumes = []
        for i in range(X.shape[0]):
            points = X[:i+1, :]
            if points.shape[0] > 3:
                hull = ConvexHull(points)
                volumes.append(hull.volume)
            else:
                volumes.append(0)

        return volumes, hull


def compute_volume_concave_hull(X, alpha, last_only=False):

    if last_only:
        concave_hull, edge_points = alpha_shape([Point(p) for p in X], alpha=alpha)
        return concave_hull.area, concave_hull, edge_points

    else:
        volumes = []
        for i in range(X.shape[0]):
            points = X[:i+1, :]
            if points.shape[0] > 3:
                concave_hull, edge_points = alpha_shape([Point(p) for p in points], alpha=alpha)
                volumes.append(concave_hull.area)
            else:
                volumes.append(0)

        return volumes, concave_hull, edge_points


def alpha_shape(points, alpha):
    """
    Compute the alpha shape (concave hull) of a set
    of points.
    @param points: Iterable container of points.
    @param alpha: alpha value to influence the
        gooeyness of the border. Smaller numbers
        don't fall inward as much as larger numbers.
        Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense
        # in computing an alpha shape.
        return MultiPoint(list(points)).convex_hull

    def add_edge(edges, edge_points, coords, i, j):
        """
        Add a line between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add((i, j))
        edge_points.append(coords[[i, j]])

    coords = np.array([point.coords[0] for point in points])
    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]
        # Lengths of sides of triangle
        a = math.sqrt((pa[0] - pb[0])**2 + (pa[1] - pb[1])**2)
        b = math.sqrt((pb[0] - pc[0])**2 + (pb[1] - pc[1])**2)
        c = math.sqrt((pc[0] - pa[0])**2 + (pc[1] - pa[1])**2)
        # Semiperimeter of triangle
        s = (a + b + c) / 2.0
        # Area of triangle by Heron's formula
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        circum_r = a * b * c / (4.0 * area)

        # Here's the radius filter.
        #print(circum_r, 1.0 / alpha)
        if circum_r < 1.0 / alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
    m = MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles), edge_points
