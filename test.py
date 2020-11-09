# -*- coding: utf-8 -*-
from random import seed
from exhaustive import exhaustive
from graham import graham
from jarvis import jarvis
from shamos import shamos
from eddy_floyd import eddy_floyd
from utils import create_points, scatter_plot

#Only set 1 to True at the time
do_exhaustive=False
do_graham=False
do_jarvis=True
do_shamos=False
do_eddy_floyd=False

def main():
    seed(0) # initialize the random generator seed to always use the same set of points
    show = True  # to display a frame
    save = False  # to save into .png files in "figs" directory 

    # creates some points
    if not do_exhaustive:
        pts = create_points(50)
        scatter_plot(pts, [[]], title="convex hull : initial set", show=show, save=save)
        print("Points:", pts)

    # compute the hull
    if do_exhaustive: 
        pts = create_points(5)
        scatter_plot(pts, [[]], title="convex hull : initial set", show=show, save=save)
        print("Points:", pts)
        hull = exhaustive(pts, show=show, save=save)
        print("Hull:", hull)
        scatter_plot(pts, [hull], title="convex hull : final result", show=True, save=save)

    if do_graham:    
        hull = graham(pts, show=show, save=save)
        print("Hull:", hull)
        scatter_plot(pts, [hull], title="convex hull : final result", show=True, save=save)

    if do_jarvis:    
        hull = jarvis(pts, show=show, save=save)
        print("Hull:", hull)
        scatter_plot(pts, [hull], title="convex hull : final result", show=True, save=save)

    if do_shamos:    
        hull = shamos(pts, show=show, save=save)
        print("Hull:", hull)
        scatter_plot(pts, [hull], title="convex hull : final result", show=True, save=save)

    if do_eddy_floyd:
        hull = eddy_floyd(pts, pts, show=show, save=save)
        print("Hull:", hull)
        scatter_plot(pts, [hull], title="convex hull : final result", show=True, save=save)


if __name__ == "__main__":
    main()
