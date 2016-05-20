import thinkdsp
#from array import array
import numpy as np
##from pylab import *
from matplotlib import pyplot as plt

valuesfile=open('abhishek_new_sensor_short2.txt','r',1)
data=[]
Fs=10.4#sampling frequency in Hz

while True:
    value=valuesfile.readline()
    #print value
    if value is '':
        break
    value=1023-int(value)
    data.append(value)

length=len(data)
print length

wave=thinkdsp.Wave(ys=data,framerate=Fs)
##spectrum=wave.make_spectrum()
wave.plot()
plt.show()
