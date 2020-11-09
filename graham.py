# -*- coding: utf-8 -*-
from utils import scatter_plot, polar_quicksort, polar_angle, modulo_360
import math

def graham(points, show=True, save=False, detailed=True):
#    :param points: the points from which to find the convex hull
#    :param show: if True, the progress in constructing the hull will be plotted on each iteration in a window
#    :param save: if True, the progress in constructing the hull will be saved on each iteration in a .png file
#    :param detailed: if True, even non convex explored polygons are plotted
    
    #If the problem is already solved, there is nothing to do
    if len(points)<3:
        print('probleme')
        return points
    
   #Find the lowest point of 'points'
    lowest=points[0]
    for p in points:
        if p[1]<lowest[1]:
            lowest=p

    #Sort the points by polar angle (using the quick-sort method) 
    points=polar_quicksort(points,lowest)  
    
    #Initialisaion    
    i=3
    hull=points[:i]
    if (show or save) and detailed:
        scatter_plot(points, [hull], title="graham search", show=show, save=save)
        print
    
    #Iterations : iteration i considers i+1 points    
    while i<len(points):
        #Put the new point at its right place in the hull        
        k=1
        while modulo_360(math.degrees(polar_angle(points[i],(hull+[hull[0]])[k-1])-polar_angle((hull+[hull[0]])[k],(hull+[hull[0]])[k-1])))<180:
            k+=1
        hull.insert(k,points[i])

        #Plot the hull (not necessarly convex at the moment)
        if (show or save) and detailed:
            scatter_plot(points, [hull], title="graham search", show=show, save=save)
            print
            
        #Delete points in order to make the hull convex        
        j=1
        while j<len(hull):
            if modulo_360(math.degrees(polar_angle(hull[j],hull[j-1])-polar_angle((hull+[hull[0]])[j+1],hull[j-1])))<180:
                hull.pop(j)
            else: j+=1
        
        #Plot the convex hull
        if (show or save):
            scatter_plot(points, [hull], title="graham search", show=show, save=save)
            print
        
        #Go to the next iteration
        i+=1
    return hull
