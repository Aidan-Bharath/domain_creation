from os import path,chdir,walk
import re
import operator as op
import glob
import numpy as np
import pandas as pd

def numSort(files,paths):
                
    if paths == '5m':
        cutLen = 6
    else:
        cutLen = 8

    #lenFiles = len(files)
    fileDict = {}
    for i,j in enumerate(files):
                    
        tFile = re.sub('.csv','',j)
        tFiles = re.sub('e','E',tFile)        
                    
        fileDict[i] = float(tFiles[cutLen:])
    
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

    #surface = height.sum()    
    
    return surface
    

def StarFindFiles(parDir):
    curDir = path.abspath('./')

    chdir(parDir)
    allConts = glob.glob('*')
    isDir = [path.isdir(dirs) for dirs in allConts]
    
    dataDirs = {}
    for paths,tf in zip(allConts,isDir):
        if tf == True:
            print paths
                
            dataPath = path.join(parDir,paths)
            chdir(dataPath)
            
            # Ugh the Sorting
            files,times = numSort(glob.glob('*'),paths)
                
            dataFiles = [path.join(dataPath,fName) for fName in files]
                
            # Unfortunitely StarCCM doesnt interpolate data so we must do that.
            sumArray = np.zeros([len(dataFiles)])                
            for index,data in enumerate(dataFiles):
                sumArray[index] = interpDF(pd.read_csv(data))
                
            dataDirs[paths] = pd.DataFrame(sumArray,index=times,columns=['vof'])
               
    chdir(curDir)
    
    return dataDirs

def OFFindFiles(parDir):
    curDir = path.abspath('./')

    chdir(parDir)
    allConts = glob.glob('*')
    isDir = [path.isdir(dirs) for dirs in allConts]

    dataDirs = []
    topPath = []
    for paths,tf in zip(allConts,isDir):
        if tf == True:
            try:
                root,dirs,files = walk(str(paths))
                data = path.join(files[0],files[-1][0])
                dataDirs.append(pd.read_csv(data,delim_whitespace=True)[3::])
                topPath.append(paths)
            except ValueError:
                print 'Data doesnt exist in '+str(paths)
                pass

    chdir(curDir)
    return dataDirs,topPath

def loadSurfFile(parDir,simType='OF',save=False):

    if simType == 'OF':
        fileLists,paths = OFFindFiles(parDir)
        dataFiles = {path:fileList for path,fileList in zip(paths,fileLists)}
        
    elif simType == 'StarCCM':
        dataFiles = StarFindFiles(parDir)

    return dataFiles

if __name__ == "__main__":

    direct = 'C://Users/ABHARATH/Documents/StarCCM/waveTank_4040/'
    files = loadSurfFile(direct,simType='StarCCM')

