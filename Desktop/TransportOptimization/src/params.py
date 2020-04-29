#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:14:37 2020
@author: weetee
"""
import math
import numpy as np
import geopy.distance as gp
from itertools import combinations

order_locs = [(1.416221, 103.870980), (1.382944, 103.893372), (1.359355, 103.886654),\
              (1.352877, 103.877846), (1.343985, 103.872836), (1.445750, 103.783694),\
              (1.398481, 103.746880), (1.306487, 103.850675), (1.303979, 103.831849),\
              (1.293550, 103.784404)]

def get_dist(coords_1, coords_2): # lat, long
    return gp.distance(coords_1, coords_2).km

def nCr(n,r):
    f = math.factorial
    return int(f(n)/(f(r)*f(n-r)))

class DataModel(object):
    def __init__(self, order_locs=[(1.416221, 103.870980), (1.382944, 103.893372), (1.359355, 103.886654),\
                                   (1.352877, 103.877846), (1.343985, 103.872836), (1.445750, 103.783694),\
                                   (1.398481, 103.746880), (1.306487, 103.850675), (1.303979, 103.831849),\
                                   (1.293550, 103.784404)],\
                order_locs_names=['a1', 'a2', 'a3',\
                                 'a4','a5','a6',\
                                 'a7','a8','a9',\
                                 'a10'],\
                pickups_deliveries=[
                                        [1, 5],
                                        [2, 6],
                                        [3, 7],
                                        [4, 8],
                                    ],\
                num_vehicles=4,\
                depot=0):
        
        self.order_locs = [(1.3, 100.3)] + order_locs # first index is dummy
        self.order_locs_names = ['dummy'] + order_locs_names
        self.start = []
        
        self.max_dist = 0.0
        self.dist_matrix = []
        for i1, l1 in enumerate(self.order_locs):
            inner = []
            for i2, l2 in enumerate(self.order_locs):
                if (i1 == 0) or (i2 == 0):
                    dist = 0.0
                else:
                    dist = get_dist(l1, l2)
                    
                if dist > self.max_dist:
                    self.max_dist = dist
                    
                inner.append(dist)
            self.dist_matrix.append(inner)
        
        self.data = {'distance_matrix': self.dist_matrix,\
                     'pickups_deliveries': pickups_deliveries,\
                     'num_vehicles': num_vehicles,\
                     'max_dist': self.max_dist,\
                     'depot': depot # dummy
                     }