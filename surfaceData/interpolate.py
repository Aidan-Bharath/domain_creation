import numpy as np
import pandas as pd


def dataDictTest(data):

    if type({}) != type(data):
        data = {'data':data}
    else:
        pass

    return data

def coreInt(data,step):

    tmax = data[:,0].max()
    timeStep = np.linspace(0,tmax,tmax*step)
    intArray = np.zeros([timeStep.shape[0],data[0,:].shape[0]])

    for i in xrange(data[0,:].shape[0]-1):
        i = i+1
        intArray[:,i] = np.interp(timeStep,data[:,0],data[:,i])

    intArray[:,0] = timeStep

    return intArray


def linearInt(data,step=100):

    data = dataDictTest(data)
    intD = {}
    for keys in data:
        colNames = data[str(keys)].columns.values.tolist()
        intData = coreInt(data[str(keys)].values,step)
        intD[str(keys)] = pd.DataFrame(intData,columns=colNames)

    return intD

if __name__ == "__main__":

    import load
    dirs = '/media/aidan/Seagate Expansion Drive/openFoam/convDatFiles'
    data = load.loadSurfFile(dirs)
    print linearInt(data)
