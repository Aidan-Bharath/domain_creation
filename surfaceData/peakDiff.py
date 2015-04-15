# -*- coding: utf-8 -*-
"""
Created on Sat Apr 04 03:09:06 2015

@author: Aidan
"""

from __future__ import division
import numpy as np
import pandas as pd
import scipy.integrate as I
import starLoad as sl
import auxFunc as aux

def waveHeightInt(data,peak,l,theoryInt=True):
    waveFiles = {}    
    for name,dat in data.iteritems():
        print name
        wave = {}         
        for i in xrange(len(peak[2][name])-1):
            plus,minus = peak[2][name][i+1],peak[2][name][i]
            dic = dat.loc[minus:plus,peak[0]]
            ln = len(dic)            
            intxy = np.zeros([ln-1])
            for j in xrange(ln-1):
                y = np.mean([dic.iloc[j+1],dic.iloc[j]])
                x = dic.index[j+1]-dic.index[j]
                intxy[j] = x*y
            wave[i] = np.sum(intxy)
        waveFiles[name] = pd.Series(wave)
    
#    if theoryInt is True:
#        x = np.linspace(0,2*np.pi,2000)
#        func = l[1]*np.cos(x)+l[5]
#        theory = np.sum(I.cumtrapz(x,func))
#        print theory
    
    return 'yes'

def squareDiff(Dir,target):

    data = [sl.loadPickle(Dir,i) for i in target] 
    sdiff = {}    
    for comb in zip(files1,files2):
        name1,name2 = aux.rmP(comb[0]),aux.rmP(comb[1])
        rms = np.sum((data[0][name1]-data[1][name2])**2/len(data[0][name1]))
        sdiff[name1+'-'+name2] = np.sqrt(rms)
    
    return pd.DataFrame(sdiff)
    
def amplitudes(Dir,target,peaks,plot=True,leg=True):
    data = [sl.loadPickle(Dir,i) for i in target]
    
    peakAmp = {}
    for i,j in peaks[2].iteritems():
        peak = data[0][i].loc[j,peaks[0]]
        peakAmp[i] = peak
    
    if plot:
        aux.dicSeriesPlot(peakAmp,leg=leg)
    
    return peakAmp
        

if __name__ == "__main__":
    
    Dir = '/media/aidan/Seagate Expansion Drive/starCCM/thickTank/pFiles/'
    #files1 = ['2mesh10-20.p','2mesh20-20.p','2mesh40-20ittc.p','2mesh60-20.p']
    #files2 = ['3mesh10-20.p','3mesh20-20.p','3mesh40-20ittc.p','3mesh60-20.p']
    files1 = ['mesh40-20ittc5x.p']    
    files2 = ['mesh40-20ittc10x.p']
    x = []
    time = []
    l = [5,0.01,1.940,x,time,1]
    data =  squareDiff(Dir,[files1,files2])
    #amp1 = amplitudes(Dir,[files2],peaks1,leg=False)
    #amp2 = amplitudes(Dir,[files2],peaks2,leg=False)
        
    
    
    