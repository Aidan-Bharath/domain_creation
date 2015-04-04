# -*- coding: utf-8 -*-
"""
Created on Sat Apr 04 03:09:06 2015

@author: Aidan
"""

from __future__ import division
import numpy as np
import pandas as pd
import scipy.integrate as I

def waveHeightInt(data,peak,l,theoryInt=True):
#    waveFiles = {}    
#    for name,dat in data.iteritems():
#        print name
#        wave = {}         
#        for i in xrange(len(peak[2][name])-1):
#            plus,minus = peak[2][name][i+1],peak[2][name][i]
#            dic = dat.loc[minus:plus,peak[0]]
#            ln = len(dic)            
#            intxy = np.zeros([ln-1])
#            for j in xrange(ln-1):
#                y = np.mean([dic.iloc[j+1],dic.iloc[j]])
#                x = dic.index[j+1]-dic.index[j]
#                intxy[j] = x*y
#            wave[i] = np.sum(intxy)
#        waveFiles[name] = pd.Series(wave)
    
    if theoryInt is True:
        x = np.linspace(0,2*np.pi,2000)
        func = l[1]*np.cos(x)+l[5]
        theory = np.sum(I.cumtrapz(x,func))
        print theory
    
    return 'yes'#pd.DataFrame(waveFiles)







if __name__ == "__main__":
    
    x = []
    time = []
    l = [5,0.01,1.940,x,time,1]
    pot = waveHeightInt(dic,peaks,l)
    #pot.plot()