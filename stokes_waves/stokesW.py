from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

class Wave:

    O = None
    g = 9.81
    pot = False
    S = None
    firsto = None
    secondo = None
    thirdo = None
    fourtho = None
    fiftho = None

    def __init__(self,lm,x,T,time,A,h=None):

        self.eta = None
        self.I = None
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


    def firstOrder(self,pot=False):

        if Wave.firsto == None:
            self.eta = self.A*np.cos(Wave.O)
            Wave.firsto = self.eta
        else:
            self.eta = Wave.firsto

        if Wave.pot == True:
            w = (Wave.omega/Wave.k)
            ch = np.cosh(self.k*(self.eta+self.h))
            sh = np.sinh(self.k*self.h)
            p = self.A*(ch/sh)*w
            self.I = p*np.sin(Wave.O)

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

    def plotWave(self):
        plt.plot(self.time,Wave.firsto.flatten()/self.k)
        plt.plot(self.time,Wave.secondo.flatten()/self.k)
        plt.plot(self.time,Wave.thirdo.flatten()/self.k)
        plt.plot(self.time,Wave.fourtho.flatten()/self.k)
        plt.plot(self.time,Wave.fiftho.flatten()/self.k)
        plt.show()



