from __future__ import division
import numpy as np

def k(l):
    return (2*np.pi)/l[0]

def omega(l):
    return (2*np.pi)/l[2]

def O(l):
    try:
        O = k(l)*l[3][:,None]-omega(l)*l[4][None,:]
    except AttributeError:
        l[4] = l[4].values
        O = k(l)*l[3][:,None]-omega(l)*l[4][None,:]
    except TypeError:
        O = k(l)*l[3]-omega(l)*l[4][None,:]
    return O


def S(l):
    return 1/np.cosh(2*k(l)*l[5])

def first(l):
    return l[1]*np.cos(O(l))

def second(l):
    B_22 = (1/np.tanh(k(l)*l[5]))*((1+2*S(l))/(2*(1-S(l))))
    return l[1]**2*B_22*np.cos(2*O(l))

def third(l):
    B_31 = -3*(1+3*S(l)+3*S(l)**2+2*S(l)**3)/(8*(1-S(l))**3)
    return l[1]**3*B_31*(np.cos(O(l))-np.cos(3*O(l)))

def fourth(l):
    coth = (1/np.tanh(k(l)*l[5]))
    num_42 = (6-26*S(l)-183*S(l)**2-204*S(l)**3-25*S(l)**4+25*S(l)**5)
    den_42 = (6*(3+2*S(l))*(1-S(l))**4)
    B_42 = coth*num_42/den_42

    num_44 = (24+92*S(l)+122*S(l)**2+66*S(l)**3+67*S(l)**4+34*S(l)**5)
    den_44 = (24*(3+2*S(l))*(1-S(l))**4)
    B_44 = coth*num_44/den_44

    return l[1]**4*(B_42*np.cos(2*O(l))+B_44*np.cos(4*O(l)))

def fifth(l):
    num_53 = 9*(132+17*S(l)-2216*S(l)**2-5897*S(l)**3-6292*S(l)**4-2687*S(l)**5+194*S(l)**6+467*S(l)**7+82*S(l)**8)
    den_53 = (128*(3+2*S(l))*(4+S(l))*(1-S(l))**6)
    B_53 = num_53/den_53

    num_55 = 5*(300+1579*S(l)+3176*S(l)**2+2949*S(l)**3+1188*S(l)**4+675*S(l)**5+1326*S(l)**6+827*S(l)**7+130*S(l)**8)
    den_55 = (384*(3+2*S(l))*(4+S(l))*(1-S(l))**6)
    B_55 = num_55/den_55

    return l[1]**5*(-(B_53+B_55)*np.cos(O(l))+B_53*np.cos(3*O(l))+B_55*np.cos(5*O(l)))

def theory(l):
    allTheory = np.zeros([l[3].shape[0],l[4].shape[0],5])

    allTheory[:,:,0] = first(l)+l[5]
    allTheory[:,:,1] = first(l)+second(l)+l[5]
    allTheory[:,:,2] = first(l)+second(l)+third(l)+l[5]
    allTheory[:,:,3] = first(l)+second(l)+third(l)+fourth(l)+l[5]
    allTheory[:,:,4] = first(l)+second(l)+third(l)+fourth(l)+fifth(l)+l[5]

    return allTheory



if __name__ == "__main__":

    lm = 5
    A = 0.015
    T = 2.389
    x = np.linspace(0,10,100)
    time = np.linspace(0,10,500)
    h = 0.5
    l = [lm,A,T,x,time,h]

    the = theory(l)
