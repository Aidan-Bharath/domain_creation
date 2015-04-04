# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 12:47:05 2015

@author: ABHARATH
"""
from __future__ import division
import sys
import scipy.signal as sig
import numpy as np
import pandas as pd
import pandas.stats.moments as mo
import re
import starLoad as sl
import auxFunc as aux

__all__ = ['peakFind','phaseError']

def peakFind(data,l,pos,order=1,_even=False):
    sets = re.sub('x',str(pos),'Report: xm (m)')
    print sets    
    iterr = 1

    while not _even:                
        iterr += 1
        mean = int(l[2]*iterr)
        maxlen = []
        phases = {}
        framepeak = {}
        for frame in data.iteritems():
            name = frame[0]
            frame = frame[1][sets]
            frameMean = mo.rolling_sum(frame**3,mean,center=True).values
            maxpeak = sig.argrelmax(frameMean,order=order)
            maxlen.append(len(maxpeak[0]))
            framepeak[name] = frame.index[maxpeak]
            phase = np.zeros([framepeak[name].shape[0]-1])
            for i in xrange(phase.shape[0]):
                phase[i] = framepeak[name][i+1]-framepeak[name][i]
            phases[name] = phase
        try:   
            phases = pd.DataFrame(phases)
            framePeaks = pd.DataFrame(framepeak)
            _even = True
        except ValueError:
            print maxlen
            print '----- All of the peaks have not been found ------'
    
    return [sets,phases,framePeaks]
     
     
def phaseError(data,peaks,l):
    pos = peaks[0]    
    l[3] = int(re.search(r'\d+',pos).group())
    theoryPeak = {}
    for name,frame in data.iteritems():
        l[4] = frame[pos].index.values
        theoryPeak[name] = frame.index[sig.argrelmax(aux.Wave(l))[0]]
    theoryPeak = pd.DataFrame(theoryPeak)
 
    peakDiff = {}
    peakDiffsd = {}
    for key in theoryPeak.keys():
        s = ((theoryPeak[key]-peaks[2][key])**2).sum()
        peakDiffsd[key] = np.sqrt(s/peaks[2][key].shape[0])
        peakDiff[key] = theoryPeak[key]-peaks[2][key]
    
    peakDiff = pd.DataFrame(peakDiff)
    peakDiffsd = pd.Series(peakDiffsd)
    
    return [peakDiff,peakDiffsd]
    
   
        



if __name__ == "__main__":

    Dir = 'C:/Users/Aidan/Documents/StarData/waveheights/'
    dic = sl.loadPickle(Dir)    
    x = []
    time = []
    l = [5,0.01,1.940,x,time,1]
    peaks = peakFind(dic,l,5)
    pE = phaseError(dic,peaks,l)
    
        