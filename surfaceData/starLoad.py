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
import blaze as bz
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

    vof = df['Volume Fraction of water']
    h = df['Z (m)']
    surface = (vof[:-1]*[h[i+1]-h[i] for i in xrange(len(h)-1)]).sum()

    return surface
    
   

def loadSurfMap(dateTime):
    
    cols = ['X (m)','Y (m)','Position[Z] (m)']
    names = ['z','x','y']
    tmp = pd.read_csv(dateTime[0],usecols=cols)
    tmp.columns = names
    return [tmp,dateTime[1]]
        

def StarFindFiles(parDir,par=8):
  
    curDir = path.abspath('./')

    chdir(parDir)
    allConts = glob.glob('*')
    isDir = [path.isdir(dirs) for dirs in allConts]
    print allConts
    
    dataDirs = {}
    for paths,tf in zip(allConts,isDir):
        if tf == True:
            print paths
                
            dataPath = path.join(parDir,paths)
            chdir(dataPath)
            
            files,times = numSort(glob.glob('*'),paths)
                
            dataFiles = [path.join(dataPath,fName) for fName in files]
             
            try:

                dataFiles = [(i,dataFiles[i]) for i in xrange(len(dataFiles))]
                p = Pool(par)                
                sumFrame = pd.DataFrame(p.map(ParintDF,dataFiles))[1]
                p.terminate()
                sumFrame = sumFrame-sumFrame.mean()
                dataDirs[paths] = sumFrame
            
            except (ValueError,KeyError):
                dateTime = [(i,j) for i,j in zip(files,times)]
                p = Pool(par)                
                load = p.map(loadSurfMap,dateTime)
                p.terminate()
            
                for i in xrange(len(load)):
                    dataDirs[load[i][1]] = load[i][0]
                
    chdir(curDir)
    
    return dataDirs

def ParintDF(df):
    
    cols = ['Volume Fraction of water','Z (m)']
    yes = interpDF(pd.read_csv(df[1],usecols=cols))
    return [df[0],yes]

if __name__ == "__main__":
    
    parDir = 'C:\Users\ABHARATH\Documents\StarCCM\ConvStudy\conv2020nbr_r'
    files = StarFindFiles(parDir)