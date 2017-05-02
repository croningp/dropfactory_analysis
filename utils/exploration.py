from shapely.geometry import Point


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
