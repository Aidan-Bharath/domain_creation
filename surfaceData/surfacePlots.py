# -*- coding: utf-8 -*-
"""
Created on Tue Mar 03 14:03:39 2015

@author: ABHARATH
"""

import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt


def setGrid(df,npoint,interp):
    xi = np.linspace(df['x'].min(),df['x'].max(),npoint)
    yi = np.linspace(df['y'].min(),df['y'].max(),npoint)
    zi = griddata((df['x'],df['y']),df['z'],(xi[None,:],yi[:,None]),method=interp)
    
    return xi,yi,zi

def Plot(df,plotshow=True,plotsave=False,npoint=500,interp='linear'):
    
    xi,yi,zi = setGrid(df,npoint,interp)
    
    plt.figure()
    
    plt.contour(xi,yi,zi,25,linewidths=0.5,colors='k')
    plt.contourf(xi,yi,zi,25,cmap=plt.cm.jet)
    plt.colorbar()
    plt.xlim(df['x'].min(),df['x'].max())
    plt.ylim(df['y'].min(),df['y'].max())
    plt.title('Tank Wave Elevation')
    
    if plotsave == True:
        import os

        Dir = '/plotDir/'
        if not os.path.exists(Dir):
            os.makedirs(Dir)
            
        plt.savefig(Dir+'plotFig',ext='png',close=False,verbose=True)
            
    if plotshow == True:
        plt.show()
    
    
    
    
    
if __name__ == "__main__":
    
    Plot(files[7.59])