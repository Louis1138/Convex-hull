# -*- coding: utf-8 -*-
from itertools import permutations
from utils import is_convex, scatter_plot, point_in_polygon

def exhaustive(points, show=True, save=False, detailed=False):
#    :param points: the points from which to find the convex hull
#    :param show: if True, the progress in constructing the hull will be plotted on each iteration in a window
#    :param save: if True, the progress in constructing the hull will be saved on each iteration in a .png file
#    :param detailed: if True, even non convex explored polygons are plotted

    i = 3
    while i <= len(points):
        #Iterates over the whole set of subset of points
        for subset in permutations(points, i):
            if (show or save) and detailed:
                scatter_plot(points, [subset], title="exhaustive search", show=show, save=save)
            #Only consider convex subsets
            if is_convex(subset):
                if (show or save) and not detailed:
                    scatter_plot(points, [subset], title="exhaustive search", show=show, save=save)
                    print
                one_out = False
                j = 0
                #Iterates until a point is found outside the polygon
                while not one_out and j < len(points):
                    point = points[j]
                    if point not in list(subset) and not point_in_polygon(point, list(subset)):
                        one_out = True
                    j = j + 1
                if not one_out:
                    return subset
        i = i + 1
    return points
