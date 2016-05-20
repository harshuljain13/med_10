import thinkdsp
#from array import array
import numpy as np
##from pylab import *
from matplotlib import pyplot as plt
from scipy import signal

valuesfile=open('Data/abhishek_new_sensor_cap.txt','r',1)
data=[]
Fs=12.5#sampling frequency in Hz, sampling interval=80 ms

while True:
    value=valuesfile.readline()
    #print value
    if value is '':
        break
    sensor=int(value)
    data.append(sensor)

length=len(data)
print "Length:", length

ptt=list(signal.correlate(data,data,mode='full')/128)
plt.plot(ptt)
plt.show()
