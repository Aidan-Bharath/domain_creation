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



if __name__ == "__main__":

    import load,theory
    import interpolate as interp
    
    Dir = 'C://Users/ABHARATH/Documents/OpenFoam'
    x = np.array([5,15,25])
    time = np.linspace(0,100,1000)
    l = [5,0.015,2.398,x,time,0.8]

    data = load.loadSurfFile(Dir)
    straightCompare(data,l,data,'gauge20',1,1)
