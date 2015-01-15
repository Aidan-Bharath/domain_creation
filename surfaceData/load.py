from os import path,chdir,walk
import glob
import numpy as np
import pandas as pd

def findFiles(parDir):
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
            except ValueError:
                print 'Data doesnt exsist in '+str(paths)
                pass
        dataDirs.append(pd.read_csv(data,delim_whitespace=True))
        topPath.append(paths)

    chdir(curDir)
    return dataDirs,topPath

def loadSurfFile(parDir):

    fileLists,paths = findFiles(parDir)
    dataFiles = {path:fileList for path,fileList in zip(paths,fileLists)}

    return dataFiles

if __name__ == "__main__":

    direct = '/media/aidan/Seagate Expansion Drive/openFoam/convDatFiles/'
    files = loadSurfFile(direct)

    print files['dat1']
