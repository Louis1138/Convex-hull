# -*- coding: utf-8 -*-
from utils import scatter_plot

#Method used:
#Return the hull in the positive sense from the point the more on the left (such as the trigonometric circle)
#Return the points p_min, p_extr and p_max found in the current iteration, not those recieved as arguments
#Return these points as arguments for next step, not in 'points'


def eddy_floyd(points, side="", p_min=[], p_max=[], show=True, save=False, detailed=True):
#    :param points: the points from which to find the convex hull
#    :param side: if "up", we care about the points above the line (p_min,p_max), else, below
#    :param p_min: the point on the left of the line (min = min abscissa)
#    :param p_max: the point on the right of the line
#    :param show: if True, the progress in constructing the hull will be plotted on each iteration in a window
#    :param save: if True, the progress in constructing the hull will be saved on each iteration in a .png file
#    :param detailed: if True, even non convex explored polygons are plotted 

    """Initial case, the pb is divided in two parts"""
    if p_min==[] or p_max==[]:
        #Find the point the most on the left (p_min) and the most on the right (p_max)
        p_min,p_max=points[0],points[0]
        for p in points:
            if p[0]<p_min[0]: p_min=p
            if p[0]>p_max[0]: p_max=p

        #Divide the points in 2 subproblems (E2=above line, E1=below line)
        #Remark: p_min and p_max are neither in E2 nore in E1        
        E1,E2=[],[]
        for p in points:
            if (p[1]-p_min[1])*(p_max[0]-p_min[0])-(p_max[1]-p_min[1])*(p[0]-p_min[0])>0: E2+=[p]
            if (p[1]-p_min[1])*(p_max[0]-p_min[0])-(p_max[1]-p_min[1])*(p[0]-p_min[0])<0: E1+=[p]
        #Go to next step and plot results, the element to return is first divided in 2 parts to plot them seperately
        to_be_returned_2=eddy_floyd(E2,side="up",p_min=p_min,p_max=p_max,show=show,save=save,detailed=detailed)
        if (show or save) and len(to_be_returned_2)>0:
            scatter_plot(points, [[p_max]+to_be_returned_2+[p_min]], title="eddy-floyd search", show=show, save=save)
        to_be_returned_1=eddy_floyd(E1,side="down",p_min=p_min,p_max=p_max,show=show,save=save,detailed=detailed)
        if (show or save) and len(to_be_returned_1)>0:
            scatter_plot(points, [[p_min]+to_be_returned_1+[p_max]], title="eddy-floyd search", show=show, save=save)
        return [p_max]+to_be_returned_2+[p_min]+to_be_returned_1

    """End algorithm ?"""
    #Find if points remain outside the line (either above if up or below if done)
    end=True
    i=0
    while end and i<len(points):
        p=points[i]
        if side=="up" and (p[1]-p_min[1])*(p_max[0]-p_min[0])-(p_max[1]-p_min[1])*(p[0]-p_min[0])>0: end=False  
        if side=="down" and (p[1]-p_min[1])*(p_max[0]-p_min[0])-(p_max[1]-p_min[1])*(p[0]-p_min[0])<0: end=False  
        i+=1

    """Intermidiate case, look for the furthest point and divide the pb in 2 pbs"""
    if not end:
        p_extr,dist=p_min,0
        E1,E2=[],[]
        if side=="up":
            #Find the furthest point from the line (above)
            for p in points:
                if (p[1]-p_min[1])*(p_max[0]-p_min[0])-(p_max[1]-p_min[1])*(p[0]-p_min[0])>dist:
                    p_extr,dist=p,(p[1]-p_min[1])*(p_max[0]-p_min[0])-(p_max[1]-p_min[1])*(p[0]-p_min[0])
                    
            #Divide the points which are still outside of the 2 lines in 2 subproblems
            for p in points:
                if (p[1]-p_extr[1])*(p_max[0]-p_extr[0])-(p_max[1]-p_extr[1])*(p[0]-p_extr[0])>0: E2+=[p]
                if (p[1]-p_min[1])*(p_extr[0]-p_min[0])-(p_extr[1]-p_min[1])*(p[0]-p_min[0])>0: E1+=[p]

            #Go to next step and plot results, the element to return is first divided in 2 parts to plot them seperately
            to_be_returned_1=eddy_floyd(E1,side=side,p_min=p_min,p_max=p_extr,show=show,save=save,detailed=detailed)
            if (show or save) and len(to_be_returned_1)>0:
                scatter_plot(points, [[p_extr]+to_be_returned_1+[p_min]], title="eddy-floyd search", show=show, save=save)
            to_be_returned_2=eddy_floyd(E2,side=side,p_min=p_extr,p_max=p_max,show=show,save=save,detailed=detailed)
            if (show or save) and len(to_be_returned_2)>0:
                scatter_plot(points, [[p_max]+to_be_returned_2+[p_extr]], title="eddy-floyd search", show=show, save=save)
            to_be_returned=to_be_returned_2+[p_extr]+to_be_returned_1
            if (show or save) and len(to_be_returned)>2:
                scatter_plot(points, [[p_max]+to_be_returned+[p_min]], title="eddy-floyd search", show=show, save=save)
                print
            return to_be_returned 

        if side=="down":
            #Find the furthest point from the line (below)          
            for p in points:
                if (p[1]-p_min[1])*(p_max[0]-p_min[0])-(p_max[1]-p_min[1])*(p[0]-p_min[0])<dist:
                    p_extr,dist=p,(p[1]-p_min[1])*(p_max[0]-p_min[0])-(p_max[1]-p_min[1])*(p[0]-p_min[0])
                    
            #Divide the points which are still outside of the 2 lines in 2 subproblems           
            for p in points:
                if (p[1]-p_min[1])*(p_extr[0]-p_min[0])-(p_extr[1]-p_min[1])*(p[0]-p_min[0])<0: E2+=[p]
                if (p[1]-p_extr[1])*(p_max[0]-p_extr[0])-(p_max[1]-p_extr[1])*(p[0]-p_extr[0])<0: E1+=[p]

            #Go to next step and plot results, the element to return is first divided in 2 parts to plot them seperately
            to_be_returned_2=eddy_floyd(E2,side=side,p_min=p_min,p_max=p_extr,show=show,save=save,detailed=detailed)
            if (show or save) and len(to_be_returned_2)>0:
                scatter_plot(points, [[p_min]+to_be_returned_2+[p_extr]], title="eddy-floyd search", show=show, save=save)
                print
            to_be_returned_1=eddy_floyd(E1,side=side,p_min=p_extr,p_max=p_max,show=show,save=save,detailed=detailed)
            if (show or save) and len(to_be_returned_1)>0:
                scatter_plot(points, [[p_extr]+to_be_returned_1+[p_max]], title="eddy-floyd search", show=show, save=save)
                print
            to_be_returned=to_be_returned_2+[p_extr]+to_be_returned_1
            if (show or save) and len(to_be_returned)>2:
                scatter_plot(points, [[p_min]+to_be_returned+[p_max]], title="eddy-floyd search", show=show, save=save)
                print
            return to_be_returned 
            
    """End case"""
    if end:
        return []

    """None of these cases"""
    print("ERREUR")
    return []

