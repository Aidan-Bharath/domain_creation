# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 12:47:05 2015

@author: ABHARATH
"""
from __future__ import division
import scipy.fftpack as fftpack
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def phaseComp(data,ext=500,sets = 'Report: 5m (m)',dic='vof'):
    interp = []        
    for dat in data:
            time = dat[dic].index.values.flatten()
            vals = dat[dic][sets].values
            interp.append([time,vals])

    newset = []
    for inter in interp:
        newtime = np.linspace(inter[0][0],inter[0][-1],inter[0].shape[0]*ext)
        newval = np.interp(newtime,inter[0],inter[1]) 
        newset.append([newtime,newval])
        
    import itertools as it
    minPhaseDiff = []
    intShift = 100
    for i,j in it.combinations(newset,2):
        error = np.zeros([intShift])
        for k in xrange(intShift):
            error[k] = np.sqrt(np.sum((i[1][k+1:]-j[1][:-(k+1)])**2)/2)
            print error[k]
        minPhaseDiff.append((np.argwhere(error==error.min())*(2/ext)).tolist())
    
    return minPhaseDiff
        
def sliceFFT(data,cut,testPhase=True):
    
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
        
        for i in xrange(len(cols)):
            dat = data[:,i]
            ps = np.abs(np.fft.fft(dat))**2
            freqs = np.fft.fftfreq(dat.shape[0],ts)
            idx = np.argsort(freqs)
            if testPhase == True:
                print abs(freqs[np.argmax(ps[idx])]*ts)
            
            plt.loglog(freqs[idx],ps[idx],label=str(cols[i]))
            plt.grid()
            plt.legend()
            plt.ylim([0.00001,10000])
        
        plt.show()


if __name__ == "__main__":

    cut = [1.000,18.000]
    sliceFFT([t5['vof']],cut)
    