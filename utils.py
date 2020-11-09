# -*- coding: utf-8 -*-
import math
import time
import os
from math import atan2  # for computing polar angle
from random import randint, sample  # for sorting and creating data pts
from matplotlib import pyplot as plt  # for plotting

def create_points(num_points, minimum=0, maximum=50):
    delta = maximum - minimum
    if delta * delta < num_points:
        raise ValueError("Number of points too large for the available space")
    ps = sample(range(0, delta * delta), num_points)
    points = []
    for p in ps:
        points.append([(p % delta) + minimum, (p // delta) + minimum])
    return points

def scatter_plot(points, convex_hulls=None, all_points=[], rays=None, minimum=0, maximum=50, title="convex hull", show=False, save=False, rep='./figs/', prefix='convexhull_'):
    fig = plt.figure(title)
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_xlim(left=minimum, right=maximum)
    ax.set_ylim(bottom=minimum, top=maximum)
    if len(all_points) > 0:
        xall, yall = zip(*all_points)  # unzip into x and y coord lists
        plt.scatter(xall, yall, c='lightgray')  # plot the data points
    xs, ys = zip(*points)  # unzip into x and y coord lists
    plt.scatter(xs, ys)  # plot the data points
    if convex_hulls is not None:
        for convex_hull in convex_hulls:
            # plot the convex hull boundary, extra iteration at
            # the end so that the bounding line wraps around
            for i in range(1, len(convex_hull) + 1):
                if i == len(convex_hull):
                    i = 0  # wrap
                c0 = convex_hull[i - 1]
                c1 = convex_hull[i]
                plt.plot((c0[0], c1[0]), (c0[1], c1[1]), 'r')
                plt.scatter((c0[0], c1[0]), (c0[1], c1[1]), c='r')
            if len(convex_hull) > 2:
                xs, ys = zip(*convex_hull)  # unzip into x and y coord lists
                plt.fill(xs, ys, 'r', alpha=0.2)
    if rays is not None:
        for ray in rays:
            for i in range(1, len(ray) + 1):
                if i == len(ray):
                    i = 0  # wrap
                c0 = ray[i - 1]
                c1 = ray[i]
                plt.plot((c0[0], c1[0]), (c0[1], c1[1]), 'darkgray', linestyle=':')
                plt.scatter((c0[0], c1[0]), (c0[1], c1[1]), c='darkgray')
    if show:
        plt.show()
    if save:
        directory = rep
        if not os.path.exists(directory):
            os.makedirs(directory)
        file = directory + prefix + repr(time.time()) + ".png"
        fig.savefig(file, bbox_inches='tight')

def point_in_polygon(point, polygon):
    x = point[0]
    y = point[1]
    n = len(polygon)
    inside = False
    xints = 0.0
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def polar_angle(point1, point2):
    y_span = point1[1] - point2[1]
    x_span = point1[0] - point2[0]
#    if x_span<0: return
    return atan2(y_span, x_span)

def distance(point1, point2):
    y_span = point1[1] - point2[1]
    x_span = point1[0] - point2[0]
    return y_span ** 2 + x_span ** 2

def norm(point1, point2):
    sum(abs(a - b) for a, b in zip(point1, point2))

def distance_from_point_to_line(point, line):
    x0 = point[0]
    y0 = point[1]
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    return abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / (
            distance(line[0], line[1]) ** 2)

def determinant(point1, point2, point3):
    return (point2[0] - point1[0]) * (point3[1] - point1[1]) - (point2[1] - point1[1]) * (point3[0] - point1[0])

def angle(point1, point2, point3):
    return math.acos((distance(point2, point1) + distance(point2, point3) - distance(point1, point3)) / (2 * math.sqrt(distance(point2, point1)) * math.sqrt(distance(point2, point3))))

def is_convex(points):
    if len(points) == 3:
        return True
    same_sign = True
    turn = angle(points[0], points[1], points[2])
    total = 180 - math.degrees(turn)
    i = 1
    while same_sign and i < len(points):
        new_turn = angle(points[(i + 0) % len(points)], points[(i + 1) % len(points)], points[(i + 2) % len(points)])
        total = 180 - math.degrees(new_turn) + total
        i = i + 1
        same_sign = (new_turn * turn) >= 0
        turn = new_turn
    return i == len(points) and total <= 360

def polar_quicksort(points, anchor):
#    :param points: the list of [x,y] points to sort
#    :param anchor: the reference point to computer polar angle
    if len(points) <= 1:
        return points
    smaller, equal, larger = [], [], []
    piv_ang = polar_angle(points[randint(0, len(points) - 1)], anchor)  # select random pivot
    for pt in points:
        pt_ang = polar_angle(pt, anchor)  # calculate current point angle
        if pt_ang < piv_ang:
            smaller.append(pt)
        elif pt_ang == piv_ang:
            equal.append(pt)
        else:
            larger.append(pt)
    return polar_quicksort(smaller, anchor) + sorted(equal, key=lambda x: distance(x, anchor)) + polar_quicksort(larger, anchor)

def modulo_360(angle):
    while angle>360:
        angle-=360
    while angle<0:
        angle+=360
    return angle
