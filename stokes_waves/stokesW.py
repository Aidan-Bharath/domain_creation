#!/usr/bin/python


from __future__ import division
import sys
import numpy as np

class Wave:

    O = None
    g = 9.81
    rho = 1000
    vk = 1.004
    pot = False
    S = None
    firsto = None
    secondo = None
    thirdo = None
    fourtho = None
    fiftho = None
    potent = None
    fluent = False
    openfoam = False

    def __init__(self,lm,x,T,time,A,h=None):

        self.eta = None
        self.I = None
        self.yp = None
        self.y = None
        self.runfile = None
        self.ofGauges = None
        self.fGauges = None
        self.ofsimtime = None
        self.fsimtime = None
        self.time = np.linspace(0,time,time*60)
        self.x = np.array([x]).flatten()
        self.lm = lm
        self.T = T
        self.A = A
        self.h = h
        self.k = (2*np.pi)/self.lm
        self.omega = (2*np.pi)/self.T
        Wave.O = self.k*self.x[:,None]-self.omega*self.time[None,:]
        Wave.S = 1/np.cosh(2*self.k*self.h)
        self.test = None

    def FOpotential(self):

        self.firstOrder()

        if Wave.potent == None:
            w = (self.omega/self.k)
            ch = np.cosh(self.k*(self.eta+self.h))
            sh = np.sinh(self.k*self.h)
            p = self.A*(ch/sh)*w
            self.I = p*np.sin(Wave.O)

            Wave.potent = self.I

        else:

            self.I = Wave.potent

    def y_plus(self,yp = 2):
        self.yp = yp

        self.FOpotential()

        gradI = np.abs(np.max(np.gradient(self.I[:,0])))/self.h
        print gradI
        u_ = np.sqrt(gradI/Wave.rho)
        self.y = [Wave.vk*self.yp/u_,self.yp]


    def firstOrder(self,pot=False):

        if Wave.firsto == None:
            self.eta = self.A*np.cos(Wave.O)
            Wave.firsto = self.eta
        else:
            self.eta = Wave.firsto

        if pot == True:
            self.FOpotential()

    def secondOrder(self,pot=False):

        if Wave.secondo == None:
            B_22 = (1/np.tanh(self.k*self.h))*((1+2*Wave.S)/(2*(1-Wave.S)))
            self.firstOrder()
            self.eta = self.eta+self.A**2*B_22*np.cos(2*Wave.O)
            Wave.secondo = self.eta
        else:
            self.eta = Wave.secondo

        #I will leave out the potential function cus i'm lazy atm

    def thirdOrder(self,pot=False):

        if Wave.thirdo == None:

            B_31 = -3*(1+3*Wave.S+3*Wave.S**2+2*Wave.S**3)/(8*(1-Wave.S)**3)

            self.secondOrder()
            self.eta = self.eta + self.A**3*B_31*(np.cos(Wave.O)-np.cos(3*Wave.O))

            Wave.thirdo = self.eta

        else:

            self.eta = Wave.thirdo

    def fourthOrder(self,pot=False):

        if Wave.fourtho == None:

            coth = (1/np.tanh(self.k*self.h))

            num_42 = (6-26*Wave.S-183*Wave.S**2-204*Wave.S**3-25*Wave.S**4+25*Wave.S**5)
            den_42 = (6*(3+2*Wave.S)*(1-Wave.S)**4)
            B_42 = coth*num_42/den_42

            num_44 = (24+92*Wave.S+122*Wave.S**2+66*Wave.S**3+67*Wave.S**4+34*Wave.S**5)
            den_44 = (24*(3+2*Wave.S)*(1-Wave.S)**4)
            B_44 = coth*num_44/den_44

            self.thirdOrder()
            self.eta = self.eta + self.A**4*(B_42*np.cos(2*Wave.O)+B_44*np.cos(4*Wave.O))

            Wave.fourtho = self.eta

        else:

            self.eta = Wave.fourtho

    def fifthOrder(self,pot=False):

        if Wave.fiftho == None:

            num_53 = 9*(132+17*Wave.S-2216*Wave.S**2-5897*Wave.S**3-6292*Wave.S**4-2687*Wave.S**5+194*Wave.S**6+467*Wave.S**7+82*Wave.S**8)
            den_53 = (128*(3+2*Wave.S)*(4+Wave.S)*(1-Wave.S)**6)
            B_53 = num_53/den_53

            num_55 = 5*(300+1579*Wave.S+3176*Wave.S**2+2949*Wave.S**3+1188*Wave.S**4+675*Wave.S**5+1326*Wave.S**6+827*Wave.S**7+130*Wave.S**8)
            den_55 = (384*(3+2*Wave.S)*(4+Wave.S)*(1-Wave.S)**6)
            B_55 = num_55/den_55

            self.fourthOrder()
            self.eta = self.eta + self.A**5*(-(B_53+B_55)*np.cos(Wave.O)+B_53*np.cos(3*Wave.O)+B_55*np.cos(5*Wave.O))

            Wave.fiftho = self.eta

        else:

            self.eta = Wave.fiftho



    def loadOFVOF(self,runfile):
        import os

        self.runfile = runfile
        pathname = os.path.abspath('/media/aidan/Seagate Expansion Drive/openFoam/')
        savePath = os.path.join(pathname+self.runfile,'gaugesVOF')
        if not os.path.isdir(savePath):
            os.makedirs(savePath)

        postPath = os.path.join(pathname+self.runfile,'/postProcessing/')
        if os.path.isdir(pathname+self.runfile+postPath):
            postPath = pathname+self.runfile+'/postProcessing/sets/'
        else:
            postPath = pathname+self.runfile+'/sets/'

        a = os.listdir(postPath)
        a.sort(lambda a,b: cmp(float(a), float(b)))

        dir1 = os.path.join(postPath,a[int(len(a)/2.0)])
        b = os.listdir(dir1)
        nSens = 0
        index = []
        for i in range(len(b)):
            test1 = b[i].find('VOF') + 1
            test2 = b[i].find('alpha') + 1
            if test1 and test2:
                index.append(i)
                nSens += 1

        self.ofGauges = np.zeros([len(index),len(a)])
        self.ofsimtime = [float(a[i]) for i in xrange(len(a))]

        if len(index) >= 10:
            print '# of Gauges exceed 10, Check file naming'
        for i,j in enumerate(a):
            for k in index:

                rfile = '/GaugeVOF0'+str(k+1)+'_alpha.water.xy'
                ofile = np.loadtxt(postPath+str(j)+rfile)

                #vof = ofile[0,2]
                vof = 0
                for s in range(len(ofile[:,1])-1):
                    vof = vof + ofile[s,3]*(ofile[s+1,1]-ofile[s,1])
                    #print vof
                self.ofGauges[k,i] = vof

        Wave.openfoam = True

    def loadFluentVOF(self,runfile):
        from glob import glob
        import pandas as pd

        self.runfile = glob(runfile)
        try:
            files = [pd.read_csv(self.runfile,delim_whitespace=True,usecols=[1,3,8]).as_matrix() for self.runfile in self.runfile]
            uni = np.unique(files[0][:,0])
            idx = []
            for i in range(len(uni)):
                a = np.argwhere(files[0][:,0] == uni[i])
                if a.shape[0] != 1:
                    idx.append(a.flatten())
            files = np.dstack(files)
            flist = [files[idx[i],:,:] for i in range(len(idx))]
        except (ValueError,IndexError):
            print 'not a combined file'
            pass
        files = glob(self.runfile+'/meshing3-*')
        files = [pd.read_csv(fle,delim_whitespace=True).as_matrix() for fle in files]

        self.fsimtime = np.linspace(0,30,6000)

        try:
            self.fGauges = np.zeros([len(flist),len(flist[0][0,0,:])])
            for i in range(len(flist)):
                a = flist[i]
                for j in range(a.shape[2]):
                    vof = 0
                    for k in range(a.shape[0]-1):
                        vof = vof + a[k,2,j]*(a[k+1,1,j]-a[k,1,j])
                    self.fGauges[i,j] = vof
        except UnboundLocalError:
            pass

        self.fGauges = np.zeros([len(files)])
        for i in xrange(len(files)):
            vof = 0
            for j in xrange(files[i].shape[0]-1):
                vof = vof + files[i][j,4]*(files[i][j+1,3]-files[i][j,3])
            self.fGauges[i] = vof


        Wave.fluent = True


    def compPlot(self,series = None): #gearing this to take a list object
        import matplotlib.pyplot as plt

        if series == None:
            try:
                series = [i for i in range(len(self.eta[:,0]))]
            except (TypeError, IndexError):
                pass
            try:
                series = [i for i in range(len(self.ofGauges[:,0]))]
            except (TypeError,IndexError):
                pass
            try:
                series = [i for i in range(len(self.fGauges[:,0]))]
            except (TypeError,IndexError):
                pass

        else:
            series = series

        plt.figure()

        tof = self.ofsimtime
        tf = self.fsimtime
        tt = self.time

        for i in range(len(series)):

            if Wave.firsto != None:
                plt.plot(tt,self.eta[i,:]+self.h,label='Stokes First-Order')

            if Wave.openfoam == True:
                plt.plot(tof,self.ofGauges[i,:],label='OpenFOAM Tank')

            if Wave.fluent == True:
                try:
                    plt.plot(tf,self.fGauges[i,:],label='Fluent Tank')
                except IndexError:
                    plt.plot(tf,self.fGauges[:],label='Fluent Tank')

            plt.legend()
            plt.grid()
            plt.xlabel(' Time (s) ')
            plt.ylabel(' Water Depth (m) ')
            plt.title('Probe Gauge Position '+str(self.x[i])+' m from Inlet')
            plt.show()


    def run(self,runfile = '/3D_tank'):
        self.runfile=runfile
        self.firstOrder()
        self.loadVOF(self.runfile)
        self.compPlot()







