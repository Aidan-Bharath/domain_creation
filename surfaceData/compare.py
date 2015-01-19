import numpy as np

def timeExtract(data):
    timeData = {key:data[key]['Time'] for key in data}
    return timeData

def theoryCompare(data,l):

    stokesOrder = ['first','second','third','fourth','fifth']

    times = timeExtract(data)
    subData = {}
    for i,j in enumerate(stokesOrder):
        temp = {}
        for key in data:
            l[4] = times[key]
            stoke = theory.theory(l)
            temp[key] = np.abs(data[key].loc[:,'gauge10'::]-stoke[:,:,i].T)
        subData[j] = temp

    return subData



if __name__ == "__main__":

    import load,theory
    import interpolate as interp

    Dir = '/media/aidan/Seagate Expansion Drive/openFoam/convDatFiles/'
    data = load.loadSurfFile(Dir)
    intData = interp.linearInt(data)
    x = np.array([10,20,30,35,40])
    time = np.linspace(0,120,1000)
    l = [8,0.05,3.0337,x,time,0.8]
    stoke = theory.theory(l)
    comp = theoryCompare(data,l)


