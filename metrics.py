#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 10:41:03 2018

@author: jojo
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as la

import matplotlib.cm as cm

def make_mask(x,y, labels):
    plot_point=[]
    for i in range(len(x)):
        if (np.isnan(x[i]) or np.isnan(y[i])):
            continue
        else:
            plot_point.append(labels[i])
    return plot_point


    

def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')
    
def pearson(x, y):
    x_bar =  np.mean(x)
    y_bar = np.mean(y)
    top = np.dot( (x-x_bar), (y-y_bar) )
    bottom = np.sqrt( sum((x - x_bar)**2) * sum((y - y_bar)**2) )
    return top/bottom


def euclid_dist(x, y):
    tot = 0
    for i in range(len(x)):
        diff = (x[i] - y[i])**2
        tot +=diff
    return np.sqrt(tot)

def man_dist(x,y):
    return sum(x-y)
    
def cos_sim(x,y):
    return np.dot(x,y) / (np.sqrt(np.sum(x**2)) * np.sqrt(np.sum(y**2)))
    
def euclid_sim(x,y):
    dist = euclid_dist(x,y)
    return 1/(1+dist)

def calc_centroid(cluster):
    """
    calculates centroid based on data in cluster
    cluster is list of feature vectors
    """
    return np.mean(cluster, axis=0)


def calc_dist_all(p_dict, dist_metric):
    """
    p_dict is list of all points key = label, value is fv
    calcualtes all the distances between all the feature vectors
    returns these distances as a dict of tuples of fvs as key, and dist as val
    """
    distances={}
    for id1,fv1 in p_dict.items():
        for id2,fv2 in p_dict.items():

            if id1==id2:
                continue

            d = dist_metric(fv1, fv2)
#            print(euclid_dist(fv1, fv2))
#            print(d)
            distances[(id1,id2)] = d
            
            
    return distances

def find_closest_pair(distances, points1, points2):
    """
    takes in dict of sample ids pairs as keys, and distances as values
    points1 list of keys in each group
    returns closest distance between points in groups
    """   
    d = np.inf
    
    for p1 in points1:
        for p2 in points2:
            if p1 == p2:
                continue
            if distances[(p1, p2)]<d:
                d = distances[(p1, p2)]
#                print(d, p1, p2)
    return d

def find_furthest_pair(distances, points1, points2):
    """
    takes in dict of sample ids pairs as keys, and distances as values
    """   
    d=0
    for p1 in points1:
        for p2 in points2:
            if p1 == p2:
                continue
            if distances[(p1, p2)]>d:
                d = distances[(p1,p2)]
    return d

def find_next_merge(distances, centroid_dict, c_dict, p_dict, linkage):
    """
    takes in dict of point distances, dict of point positions, and linkage
    """   

    d_tup=(np.inf, 0,0)

    for cid1 in centroid_dict.keys():
        for cid2 in centroid_dict.keys():
            if cid1==cid2:
                continue
            points1 = c_dict[cid1]
            points2 = c_dict[cid2]
            if linkage=='min':
                d = find_closest_pair(distances, points1, points2)
            else:
                d = find_furthest_pair(distances, points1, points2)
            if d<d_tup[0]:
                d_tup = d, cid1, cid2
        
    return d_tup


def link_WPGMC(c1, c2):
    """
    takes in two clusters, calcuates new merged cluster centroid 
    based on mean of two previous centroids
    returns coords of new centroid
    """
    c1_centroid = calc_centroid(c1)
    c2_centroid = calc_centroid(c2)
    return np.mean([c1_centroid, c2_centroid], axis=0)

def link_UPGMC(c1, c2):
    """
    takes in two clusters, calculates new merged cluster centroid
    based on members of both clusters
    """
    c1.append(c2)
    return calc_centroid(c1)

def plot_grouping(centroid_dict, p_dict,ax_lims, d=0):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.axis=ax_lims
    plt.grid()
    colors = cm.rainbow(np.linspace(0, 1, len(centroid_dict.keys())))
    
    for cent, lab in zip(p_dict.values(), p_dict.keys()):
        plt.plot(cent[0], cent[1], 'k.')
        ax.annotate(lab, xy = cent)
                    
    for cent, c in zip(centroid_dict.values(), colors):
        plt.scatter(cent[0], cent[1], color=c, alpha=0.3, s=((d+1)*5)**4)
    plt.show()
    
def hac(X, labels, dist_metric, min_or_max, centroid_calc):

    p_dict = {}
    c_dict = {}
    centroid_dict={}
    for i in range(len(X)):
        centroid_dict[i] = X[i] # sets each point as centroid
        p_dict[labels[i]] = X[i] #sets name for each data point
        c_dict[i] = [labels[i]] #stores which points are associated with which centroid
    distances=calc_dist_all(p_dict, dist_metric) #works out all the distances between points
    merge_order=[]
    next_cid = len(centroid_dict.keys())
    plot_grouping(centroid_dict, p_dict, [-2.25, 2.25, -1,2])
    while len(centroid_dict.keys())>1:

        d, c1, c2 = find_next_merge(distances, centroid_dict, c_dict, p_dict, min_or_max)

        pid_list1 = c_dict[c1]
        pid_list2 = c_dict[c2]

        clust1 = [p_dict[p_id] for p_id in pid_list1]
        clust2 = [p_dict[p_id] for p_id in pid_list2]

        new_centroid = centroid_calc(clust1, clust2)
        centroid_dict[next_cid] = new_centroid
        c_dict[next_cid] = pid_list1 + pid_list2
        del centroid_dict[c1]
        del centroid_dict[c2]
        plot_grouping(centroid_dict, p_dict, [-2.25, 2.25, -1,2], d)


        next_cid +=1
        merge_order.append((d, pid_list1, pid_list2))
    return merge_order, p_dict

def plot_dentrogram(merge_order, p_dict):
    """
    somehow plots a dendrogram for the merge order given
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xlabel("distance")
    plt.ylabel("data points")
    y = [x for x in range(len(p_dict))]
    x = np.zeros(len(y))
    labels = p_dict.keys()
    for point, lab in zip(y,labels):
        plt.plot(0, point, 'k.')
        ax.annotate(lab, xy=(0,point))
    for d, pid_list1, pid_list2 in merge_order:
        for point, lab in zip(y,labels):
            plt.plot(d, point, 'k.')

        
        
    
        
X = np.array([[1.5,1.5], [2,1],[-2.01,0.5], [-1,0.5], [-1,-0.5],  [-1.5,-0.5]])
#print(metrics.calc_dist_all(X, metrics.euclid_dist))
labels=['A', 'B', 'C', 'D', 'E', 'F']
mo, p_dict = hac(X, labels, euclid_dist, 'max', link_WPGMC)

plot_dentrogram(mo, p_dict)

#
#hac(X, labels, euclid_dist, 'max', link_WPGMC)