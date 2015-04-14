# -*- coding: utf-8 -*-
"""
Created on Tue Apr 07 15:44:29 2015

@author: ABHARATH
"""

from __future__ import division
from os import path,chdir
import os
import pandas as pd
import re
import operator as op
import glob


__all__ = ['FindFilesCluster']

def _numSort(files,paths):
                
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
    
def _loadDF(df):
    
    #cols = ['Volume Fraction of water','Z (m)']
    data = pd.read_csv(df,nrows=1).values[:,:-3].flatten()    
    return data
    
def _loadSurfMap(dateTime):
    
    cols = ['X (m)','Y (m)','Position[Z] (m)']
    names = ['z','x','y']
    tmp = pd.read_csv(dateTime[0],usecols=cols)
    tmp.columns = names
    return [tmp,dateTime[1]]
    
def FindFilesCluster(surfFile=False):
  
    parDir = os.getcwd()
    filedir = path.split(parDir)[-1]
    
    allConts = glob.glob('*')
    isDir = [path.isdir(dirs) for dirs in allConts]

    dataDirs = {}
    for paths,tf in zip(allConts,isDir):
        if tf == True:
                
            dataPath = path.join(parDir,paths)
            chdir(dataPath)
            
            files,times = _numSort(glob.glob('*'),paths)
                
            dataFiles = [path.join(dataPath,fName) for fName in files]
             
            if surfFile == False:
                header = pd.read_csv(dataFiles[0],nrows=1).columns[:-3]
                sumFrame = [_loadDF(data) for data in dataFiles]
                sumFrame = pd.DataFrame(sumFrame,index=times,columns=header)
                dataDirs[filedir+str(' ')+paths] = sumFrame
            
            else:
                dateTime = [(i,j) for i,j in zip(files,times)]
                load = [_loadSurfMap(data) for data in dateTime]
            
                for i in xrange(len(load)):
                    dataDirs[load[i][1]] = load[i][0]

    print 'End Time '+str(times[-1])
    chdir(parDir)
    return dataDirs
    
def savePickle(data):
    data[data.keys()[0]].to_pickle(data.keys()[0]+'.p')
    
    
if __name__ == "__main__":
    
    data = FindFilesCluster()
    savePickle(data)