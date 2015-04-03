# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 12:47:05 2015

@author: ABHARATH
"""
from __future__ import division
import scipy.fftpack as fftpack
import scipy as sp
import scipy.signal as sig
import scipy.ndimage.measurements as mes
import numpy as np
import pandas as pd
import pandas.stats.moments as mo
import re
import matplotlib.pyplot as plt
import starLoad as sl


def _k(l):
    return (2*np.pi)/l[0]

def _omega(l):
    return (2*np.pi)/l[2]

def _O(l):
    return _k(l)*l[3]-_omega(l)*l[4]

def Wave(l):
    return l[1]*np.cos(_O(l))+l[5]


def peakFind(data,l,pos,order=5):
    mean = int(l[2]*100)
    sets = re.sub('x',str(pos),'Report: xm (m)')
    print sets    
    phases = {}
    framepeak = {}
    for frame in data.iteritems():
        name = frame[0]
        frame = frame[1][sets]
        frameMean = mo.rolling_sum(frame**3,mean,center=True).values
        maxpeak = sig.argrelmax(frameMean,order=order)
        framepeak[name] = frame.index[maxpeak]
        phase = np.zeros([framepeak[name].shape[0]-1])
        for i in xrange(phase.shape[0]):
            phase[i] = framepeak[name][i+1]-framepeak[name][i]
        phases[name] = phase
    phases = pd.DataFrame(phases)
    framePeaks = pd.DataFrame(framepeak)

    
    return [sets,phases,framePeaks]
     
def phaseError(data,peaks,l):
    pos = peaks[0]    
    l[3] = int(re.search(r'\d+',pos).group())
    theoryPeak = {}
    for name,frame in data.iteritems():
        l[4] = frame[pos].index.values
        theoryPeak[name] = frame.index[sig.argrelmax(Wave(l))[0]]
    theoryPeak = pd.DataFrame(theoryPeak)
 
    peakDiff = {}
    peakDiffsd = {}
    for key in theoryPeak.keys():
        s = ((theoryPeak[key]-peaks[2][key])**2).sum()
        peakDiffsd[key] = s/peaks[2][key].shape[0]
        peakDiff[key] = theoryPeak[key]-peaks[2][key]

    peakDiff = pd.DataFrame(peakDiff)
    pea = pd.DataFrame(peakDiffsd)
    
    return data
    
   
        
def sliceFFT(data,cut,testPhase=True,norm=False):
    
    if len(data) != 1:
        for datas,slices in zip(data,cut):
            datas = datas.ix[slices[0]:slices[1]]
            cols = datas.columns
            ts = datas.index[1]-datas.index[0]
            datas = datas.values
            
            ps = np.fft.fft(datas)**2            
            freqs = np.fft.fftfreq(datas.shape[0],ts)
            idx = np.argsort(freqs)

            for i in xrange(len(cols)):
                plt.plot(freqs[idx],ps[idx,i],label=str(cols[i]))
            plt.show()
        
    else:
        data = data[0].ix[cut[0]:cut[1]]
        cols = data.columns
        ts = data.index[1]-data.index[0]
        data = data.values
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for i in xrange(len(cols)):
            dat = data[:,i]
            ps = np.abs(np.fft.fft(dat-dat.mean()))**2
            freqs = np.fft.fftfreq(dat.shape[0],ts)
            idx = np.argsort(freqs)
            if testPhase == True:
                print abs(freqs[np.argmax(ps[idx])]*ts)
            if norm == True:
                psmax = ps.max()
                psmin = ps.min()
                
            
            ax.plot(freqs[idx],ps[idx],label=str(cols[i]))
            #plt.grid()
            #plt.legend()
            #plt.ylim([0.00001,10000])
            ax.set_yscale('log')
            #ax.set_xlim([0.2,2])
            #ax.set_ylim([0.01,1000])
            ax.grid()
            plt.legend()
        plt.show()


if __name__ == "__main__":

    Dir = 'C:/Users/ABHARATH/Documents/StarCCM/tank50m3/'
    files = ['mesh10-20.p','mesh20-20.p','mesh40-05.p','mesh40-10.p','mesh40-20ittc.p']
    dic = sl.loadPickle(Dir,files)    
    x = []
    time = []
    l = [5,0.01,1.940,x,time,1]
    peaks = peakFind(dic,l,10)
    phaseError = phaseError(dic,peaks,l)
    
    #cut = [2.000,18.000]
    #sliceFFT([t3['vof']],cut)
    