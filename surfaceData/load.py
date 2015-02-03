from os import path,chdir,walk
import glob
import numpy as np
import pandas as pd

def interpDF(df):
    # Meant to specifically work on StarCCM data

    height = np.zeros([len(df['Z (m)'])-1])

    for i in xrange(height.shape[0]):
        vof = df['Volume Fraction of Water'][i]
        h = df['Z (m)'][i+1]-df['Z (m)'][i]
        height[i] = vof*h

    surface = height.sum()    
    
    return surface
    

def StarFindFiles(parDir):
    curDir = path.abspath('./')
    
    # Unfortunitely StarCCM doesnt interpolate data so we must do that.

    chdir(parDir)
    allConts = glob.glob('*')
    isDir = [path.isdir(dirs) for dirs in allConts]
    
    dataDirs = {}
    for paths,tf in zip(allConts,isDir):
        if tf == True:
                dataPath = path.join(parDir,paths)
                chdir(dataPath)

                #Watch out here the sorting is not correct
                files = sorted(glob.glob('*'))
                dataFiles = [path.join(dataPath,fName) for fName in files]
                sumArray = np.zeros([len(dataFiles)])                
            
                for index,data in enumerate(dataFiles):
                    sumArray[index] = interpDF(pd.read_csv(data))
                
                
                dataDirs[paths] = pd.DataFrame(sumArray)
               
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

def loadSurfFile(parDir,simType='OF'):

    if simType == 'OF':
        fileLists,paths = OFFindFiles(parDir)
        dataFiles = {path:fileList for path,fileList in zip(paths,fileLists)}
        
    elif simType == 'StarCCM':
        dataFiles = StarFindFiles(parDir)

    return dataFiles

if __name__ == "__main__":

    direct = 'C://Users/ABHARATH/Documents/StarCCM/waveTank_4040/'
    files = loadSurfFile(direct,simType='StarCCM')

