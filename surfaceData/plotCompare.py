from __future__ import division
import numpy as np
import pandas as pd
import theory
import matplotlib.pyplot as plt

def straightCompare(data,l,mesh='dat1',gauge='gauge10',position=0,sOrder=1):
    if type('') == type(mesh):
        data = data[mesh]

        import theory
        l[4] = data.loc[:,'Time']
        stokes = theory.theory(l)

        fig = plt.figure()
        plt.plot(l[4],stokes[position,:,sOrder-1],label='Stokes Order '+str(sOrder))
        plt.plot(l[4],data.loc[:,gauge],label=mesh)
        plt.legend(loc=4)
        plt.show()

    elif type({}) == type(mesh):
        import operator
        length = {key:len(data[key]) for key in data}
        maxLen = str(max(length.iteritems(),key=operator.itemgetter(1))[0])

        import theory
        l[4] = data[maxLen].loc[:,'Time']
        stokes = theory.theory(l)

        fig = plt.figure()
        plt.plot(l[4],stokes[position,:,sOrder-1],label='Stokes Order '+str(sOrder))

        for key in data:
            plt.plot(data[key].loc[:,'Time'],data[key].loc[:,gauge],label=key)

        plt.legend(loc=4)
        plt.grid()
        plt.title(gauge)
        plt.show()

def findTimes(data):
    time = data['thin'].index.values.flatten()
    return time
    
def cutData(data):
    data = data[0][data[1]][data[2]]
    return data
    
def dataDiff(data,i,j):
    data = (((data[i]-data[j])**2).apply(np.sum)).apply(np.sqrt)
    return data
    
def calcDiff(data):
    import itertools as it
    for col in it.combinations(data.columns,2):
        data[str(i)+'-'+str(j)] = dataDiff(data,col[0],col[1])
    
    frameLen = len(data.columns)
    for i in xrange(frameLen):
        if i != frameLen-1:
            for j in xrange(frameLen-(i)):
                j = j+i
                if (j != frameLen and i != j):
                    data[str(i)+'-'+str(j)] = dataDiff(data,i,j)
                    
    return data
    
def compTheory(data,position=0,order=1):
    rms = []
    recur = 500
    shift = np.linspace(0,2*np.pi,recur)
    time = data[0][0].index.values.flatten()
    l = data[1][1]
        
    for i in xrange(recur):    
    
        l[4] = time-shift[i]
        the = theory.theory(l)[position,:,order]
        a = np.sqrt(np.sum((data[0][0]-the)**2)/len(data[0][0]))
        rms.append(a)

    rms = np.array(rms)
    rms_shift = np.argwhere(rms == rms.min())
    l[4] = (time-shift[rms_shift]).flatten()
      
    return theory.theory(l)[position,:,order]



def starCalc(data,l,diff=True,thry=True):    
    from multiprocessing import Pool
    
    cols = ['t1','t2','t3','t4']
    probe = 'Report: 5m (m)'
    name = 'thin'
    
    p = Pool(8)
    
    data = [(dat,name,probe) for dat in data]
    data = p.map(cutData,data)
    p.terminate()
      
    data = pd.concat(data,axis=1)
    data.columns = cols

    if thry == True:
        compdata = [(data.iloc[:,i],l) for i in xrange(len(data.columns))]
        data['theory'] = compTheory(compdata)    
      
    if diff == True:
        data = calcDiff(data)
        
    return [data,probe,cols]
   
def starPlot(data,l,diff=True,thry=True):
    data,probe,cols = data[0],data[1],data[2]
    
    if diff and thry == True:
        cols.append('theory')
        lcols = len(cols)
        time = data.index.values 
        
        plt.subplot(211)
        plt.plot(time,data.iloc[:,:lcols],label=cols)
        plt.title('Waveheight '+str(probe))
        plt.grid()
        plt.legend()
        plt.subplot(212)
        plt.plot(time,data.iloc[:,lcols+1:])
        plt.grid()        
        plt.show()
        

if __name__ == "__main__":

    Dir = 'C://Users/ABHARATH/Documents/OpenFoam'
    x = np.array([5])
    time = np.linspace(0,100,1000)
    l = [5,0.01,1.940,x,time,1]
    data = starCalc([t1,t2,t3,t4],l)
    starPlot(data,l)
    

    
