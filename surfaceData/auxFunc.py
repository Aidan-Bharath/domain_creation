# -*- coding: utf-8 -*-
"""
Created on Sat Apr 04 03:17:15 2015

@author: Aidan
"""

import numpy as np
import re
import matplotlib.pyplot as plt

__all__ = ['Wave','rmP','dicSeriesPlot','dicDFSlice']

def _k(l):
    return (2*np.pi)/l[0]

def _omega(l):
    return (2*np.pi)/l[2]

def _O(l):
    return _k(l)*l[3]-_omega(l)*l[4]

def Wave(l):
    return l[1]*np.cos(_O(l))+l[5]
    
def rmP(name):
    return re.sub('.p','',name)
    
def dicSeriesPlot(dic,leg=True):
    for i,j in dic.iteritems():
        plot = j.plot(label=i)
    if leg:
        plt.legend()
            
    return plot
    
def dicDFSlice(dic,time):
    for name,data in dic.iteritems():
        dic[name] = data.loc[:time,:]
        
    return dic