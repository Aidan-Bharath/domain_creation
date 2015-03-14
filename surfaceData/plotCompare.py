from __future__ import division
import numpy as np
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

def starPlot(data1,data2,l):
    import theory    
    
    time1 = data1['thin']['Report: 15m (m)'].index.values.flatten()
    time2 = data2['thin']['Report: 15m (m)'].index.values.flatten()
    data1 = data1['thin']['Report: 15m (m)'].values.flatten()
    data2 = data2['thin']['Report: 15m (m)'].values.flatten()
    #time1 = data1['thin']['Report: 15m (m)'][5.000:15.000].index.values.flatten()
    #time2 = data2['thin']['Report: 15m (m)'][5.000:15.000].index.values.flatten()
    #data1 = data1['thin']['Report: 15m (m)'][5.000:15.000].values.flatten()
    #data2 = data2['thin']['Report: 15m (m)'][5.000:15.000].values.flatten()
    #rms = np.sqrt(np.sum((data1-data2)**2)/len(data1))
    
    recur = 1000
    shift = np.linspace(0,2,recur)
      
    trms1=[]
    trms2=[]
    for i in xrange(recur):
        l[4] = time1+shift[i]
        the = theory.theory(l)
        trms1.append(np.sqrt(np.sum((data1-the[:,:,1])**2)/len(data1)))
        l[4] = time2+shift[i]
        the = theory.theory(l)
        trms2.append(np.sqrt(np.sum((data2-the[:,:,1])**2)/len(data2)))
    
    ts1 = np.argwhere(np.array(trms1) == np.array(trms1).min())
    ts2 = np.argwhere(np.array(trms2) == np.array(trms2).min())
    print l[2] - shift[ts1]
    print l[2] - shift[ts2]    
    
    l[4] = time1
    
    stokes = theory.theory(l)
    #print rms
    
    font = {'family':'normal','weight':'bold','size':20}
    plt.rc('font',**font)
    fig = plt.figure()
    plt.plot(time1,data1,label='Laminar Model')
    plt.plot(time2,data2,label='RSM Model')
    #plt.plot(time1,stokes[:,:,1].flatten(),label='Stokes 2nd-Order')
    plt.legend(loc=3)
    plt.grid()
    plt.title('Wave Elevation')
    plt.xlabel('Time (s)')
    plt.ylabel('Water Elevation (m)')
    plt.show()
    

if __name__ == "__main__":

    import load,theory
    import interpolate as interp
    
    Dir = 'C://Users/ABHARATH/Documents/OpenFoam'
    x = np.array([5])
    time = np.linspace(0,100,1000)
    l = [5,0.1,1.940,x,time,1]
    starPlot(files1,files2,l)

    
