# -*- coding: utf-8 -*-
import math
#I have added the function modulo_360 to utils: motulo_360(teta) is in [0,360] and is equal to teta modulo 360
from utils import scatter_plot, polar_angle, modulo_360

def jarvis(points, show=True, save=False, detailed=True):
#    :param points: the points from which to find the convex hull
#    :param show: if True, the progress in constructing the hull will be plotted on each iteration in a window
#    :param save: if True, the progress in constructing the hull will be saved on each iteration in a .png file
#    :param detailed: if True, even non convex explored polygons are plotted

    #Find the lowest point of 'points'
    lowest=points[0]
    for p in points:
        if p[1]<lowest[1]: lowest=p
    
    #Initiate the hull with 'lowest' which necessarly is in the convex hull (because it is the lowest point)
    hull=[lowest]

    #Each iteration will find the next point of the hull 
    done=False
    while not done:
        #Start with any point different from hull[-1] (to be able to get the mesure of an angle)
        next_point=points[0]
        if next_point==hull[-1]: next_point=points[1]

        #Find the next point of the convex hull by looking for the point "the most on the right" from hull[-1] point of vue
        for p in points:
            if p!=hull[-1] and modulo_360(math.degrees(polar_angle(p,hull[-1])-polar_angle(next_point,hull[-1])))>180: next_point=p

        #Add the new point to 'hull'
        hull+=[next_point]
        
        #Test if the hull is complete or if the loop needs to continue
        done=next_point==hull[0]
        
        #Plot the current form of the hull
        if (show or save):
            scatter_plot(points, [hull], title="jarvis search", show=show, save=save)
            print
    return hull
