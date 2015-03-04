# -*- coding: utf-8 -*-
"""
Created on Tue Mar 03 15:20:56 2015

@author: ABHARATH
"""

import numpy
import pylab
import pandas

from pywt import WaveletPacket

x = numpy.arange(612 - 80, 20, -0.5) / 150.
data = numpy.sin(20 * pylab.log(x)) * numpy.sign((pylab.log(x)))
from sample_data import ecg as data
print data
#data = files['5m'].values.flatten().tolist()
#print data
data = numpy.sin(numpy.power(numpy.linspace(-10,10,1000),4))
wp = WaveletPacket(data, 'sym5', maxlevel=8)

pylab.bone()
pylab.subplot(wp.maxlevel + 1, 1, 1)
pylab.plot(data, 'k')
pylab.xlim(0, len(data) - 1)
pylab.title("Wavelet packet coefficients")

for i in range(1, wp.maxlevel + 1):
    ax = pylab.subplot(wp.maxlevel + 1, 1, i + 1)
    nodes = wp.get_level(i, "freq")
    nodes.reverse()
    labels = [n.path for n in nodes]
    values = -abs(numpy.array([n.data for n in nodes]))
    print values.shape
    pylab.imshow(values, interpolation='nearest', aspect='auto')
    pylab.yticks(numpy.arange(len(labels) - 0.5, -0.5, -1), labels)
    pylab.setp(ax.get_xticklabels(), visible=False)

#pylab.show()
