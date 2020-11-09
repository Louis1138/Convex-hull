# -*- coding: utf-8 -*-
from graham import graham


def shamos(points, show=True, save=False, detailed=True):
#    :param points: the points from which to find the convex hull
#    :param show: if True, the progress in constructing the hull will be plotted on each iteration in a window
#    :param save: if True, the progress in constructing the hull will be saved on each iteration in a .png file
#    :param detailed: if True, even non convex explored polygons are plotted

    #Prétraitement : sort points by abscissa
    points.sort()

    #Condition to stop
    l=len(points)
    if l<=3:
        return points
    
    #Else, the problem is divided in 2 subproblems and the merged with the graham method
    return graham(shamos(points[:l//2],show=show,save=save,detailed=detailed)+shamos(points[l//2:],show=show,save=save,detailed=detailed),show=show,save=save,detailed=detailed)
