# -*- coding: utf-8 -*-
"""
Created on Fri Mar 06 14:05:36 2015

@author: ABHARATH
"""

import numpy as np
import pandas as pd
import blaze as bz
import pywt as wt



def calc2D(data,npoints=1000,interp='linear'):
    from surfacePlots import setGrid
    
    [xi,yi,zi] = setGrid(data,npoints,interp)
    grid = [xi,yi,zi]
    coef = wt.dwt2(zi,'db1')


    return coef,grid


if __name__ == "__main__":
    
    a,b = calc2D(files[7.59])
    