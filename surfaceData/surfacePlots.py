# -*- coding: utf-8 -*-
"""
Created on Tue Mar 03 14:03:39 2015

@author: ABHARATH
"""

import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib import cm


def setGrid(df,npoint,interp):
    xi = np.linspace(df['x'].min(),df['x'].max(),npoint)
    yi = np.linspace(df['y'].min(),df['y'].max(),npoint)
    zi = griddata((df['x'],df['y']),df['z'],(xi[None,:],yi[:,None]),method=interp)
    
    return xi,yi,zi

def surfPlot(df,plotshow=True,plotsave=False,npoint=1000,interp='linear'):
    
    xi,yi,zi = setGrid(df,npoint,interp)
    
    plt.figure()
    
    plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
    plt.contourf(xi,yi,zi,100,cmap=plt.cm.jet)
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
    
def dwt2Plot(data,degr=False,plotsave=False,npoint=500,interp='linear'):
    import waveletCalc as wC
    
    coef,grid = wC.calc2D(data,npoint,interp)
    
    if degr is not True:
        plt.figure()
        
        plt.contour(grid[0][::2],grid[1][::2],coef[1][2],25,linewidths=0.5,colors='k')
        plt.contourf(grid[0][::2],grid[1][::2],coef[1][2],25,cmap=plt.cm.jet)
        plt.colorbar()
        plt.xlim(grid[0].min(),grid[0].max())
        plt.ylim(grid[1].min(),grid[1].max())
        plt.title('Tank Wave Elevation')
        
        plt.show()
       
    if degr is True:
        from mpl_toolkits.mplot3d import axes3d
       
        x = np.tile(grid[0][::2],(grid[0][::2].shape[0],1))        
        y = np.tile(grid[1][::2],(grid[1][::2].shape[0],1))        
        z = coef[0]+coef[1][0]+coef[1][1]+coef[1][2]            
        
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(x,y.T,z,rstride=10,cstride=10,cmap=cm.coolwarm)
        fig.colorbar(surf,shrink=0.5,aspect=5)
        
        plt.show()
    
    
    return coef,grid
    
    
def gridplotTest(numiter=1000):
    import pywt as wt

    ds = 50
    
    l = np.linspace(1,5,ds)
    A = np.random.rand(ds,ds)
    w = np.random.rand(ds,ds)
    clear = np.tile(l,(ds,1))
    clear = 0.5*np.sin(2*np.pi*clear)   
    sign1 = A*np.sin(np.sqrt(2*np.pi*l+(2+w)))
    sign2 = A*np.sin((5*np.pi*l)**2-w)/l**2
    xi = np.linspace(1,5,len(l))
    yi = np.linspace(1,5,len(l))
    
      
    sign = sign1+sign2+clear
        
    coef = wt.wavedec2(sign,'db1',level=1)
    print coef[0].shape

    plt.figure()
    plt.subplot(321)
    plt.contour(xi,yi,sign,25,linewidths=0.5,colors='k')
    plt.contourf(xi,yi,sign,25,cmap=plt.cm.jet)
    plt.colorbar()
    plt.xlim(1,5)
    plt.ylim(1,5)
    plt.title('Tank Wave Elevation')
    
    coeftotal = coef[0]+coef[1][0]+coef[1][1]+coef[1][2] 
    print coeftotal.shape
    
    plt.subplot(322)
    plt.contour(xi[::2],yi[::2],coeftotal,25,linewidths=0.5,colors='k')
    plt.contourf(xi[::2],yi[::2],coeftotal,25,cmap=plt.cm.jet)
    plt.colorbar()
    plt.xlim(1,5)
    plt.ylim(1,5)
    plt.title('total components')
    
    plt.subplot(323)
    plt.contour(xi[::2],yi[::2],coef[0],25,linewidths=0.5,colors='k')
    plt.contourf(xi[::2],yi[::2],coef[0],25,cmap=plt.cm.jet)
    plt.colorbar()
    plt.xlim(1,5)
    plt.ylim(1,5)
    plt.title('average')
    
    plt.subplot(324)    
    plt.contour(xi[::2],yi[::2],coef[1][0],25,linewidths=0.5,colors='k')
    plt.contourf(xi[::2],yi[::2],coef[1][0],25,cmap=plt.cm.jet)
    plt.colorbar()
    plt.xlim(1,5)
    plt.ylim(1,5)
    plt.title('wavelet space horzontal')
    
    plt.subplot(325)    
    plt.contour(xi[::2],yi[::2],coef[1][1],25,linewidths=0.5,colors='k')
    plt.contourf(xi[::2],yi[::2],coef[1][1],25,cmap=plt.cm.jet)
    plt.colorbar()
    plt.xlim(1,5)
    plt.title('wavelet space vertical')    
    plt.ylim(1,5)

    plt.subplot(326)    
    plt.contour(xi[::2],yi[::2],coef[1][2],25,linewidths=0.5,colors='k')
    plt.contourf(xi[::2],yi[::2],coef[1][2],25,cmap=plt.cm.jet)
    plt.colorbar()
    plt.xlim(1,5)
    plt.ylim(1,5)
    plt.title('wavelet space diagonal')    
    plt.show()
        
if __name__ == "__main__":
    
    surfPlot(dif[7.95]) 
    #coef,grid = dwt2Plot(dif[9.43],degr=True)