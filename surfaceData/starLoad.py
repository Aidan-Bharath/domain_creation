# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 20:25:19 2015

@author: Aidan
"""
from os import path,chdir
import re
import operator as op
import glob
import numpy as np
import pandas as pd
from multiprocessing import Pool


def numSort(files,paths):
                
    fileDict = {}
    for i,j in enumerate(files):
                    
        tFile = re.sub('.csv','',j)
        tFile = tFile[-12:]
        tFiles = re.sub('e','E',tFile)        
        
        fileDict[i] = float(tFiles)
    
    testDict = sorted(fileDict.items(),key=op.itemgetter(1))
    
    files = [files[item[0]] for item in testDict]
    times = [item[1] for item in testDict]
    
    return files,times
    

def interpDF(df):
    # Meant to specifically work on StarCCM data

    height = np.zeros([len(df['Z (m)'])-1])
    surface = 0
    for i in xrange(height.shape[0]):
        vof = df['Volume Fraction of Water'][i]
        h = df['Z (m)'][i+1]-df['Z (m)'][i]
        surface = surface + vof*h

    return surface
    

def loadSurfMap(dateTime):
    
    cols = ['X (m)','Y (m)','Z (m)']
    names = ['x','y','z']
    tmp = pd.read_csv(dateTime[0],usecols=cols)
    tmp.columns = names
    return [tmp,dateTime[1]]
        

def StarFindFiles(parDir,pool=2):
    curDir = path.abspath('./')

    chdir(parDir)
    allConts = glob.glob('*')
    isDir = [path.isdir(dirs) for dirs in allConts]
    
    dataDirs = {}
    for paths,tf in zip(allConts,isDir):
        if tf == True:
                
            dataPath = path.join(parDir,paths)
            chdir(dataPath)
            
            # Ugh the Sorting
            files,times = numSort(glob.glob('*'),paths)
                
            dataFiles = [path.join(dataPath,fName) for fName in files]
                
            # Unfortunitely StarCCM doesnt interpolate data so we must do that.
            try:
                sumArray = np.zeros([len(dataFiles)])                
                for index,data in enumerate(dataFiles):
                    sumArray[index] = interpDF(pd.read_csv(data))
                
                dataDirs[paths] = pd.DataFrame(sumArray,index=times)
            
            except (ValueError,KeyError):
                dateTime = [(i,j) for i,j in zip(files,times)]
                p = Pool()                
                load = p.map(loadSurfMap,dateTime)
                p.terminate()
                
                for i in xrange(len(load)):
                    dataDirs[load[i][1]] = load[i][0]
                
    chdir(curDir)
    
    return dataDirs


if __name__ == "__main__":
    
    parDir = 'C:\Users\Aidan\My Documents\StarData'
    files = StarFindFiles(parDir)