# -*- coding: utf-8 -*-
"""
Created on Sat Apr 04 03:01:34 2015

@author: Aidan
"""



from __future__ import division
import scipy.fftpack as fftpack
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import starLoad as sl



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