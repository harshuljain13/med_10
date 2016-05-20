import thinkdsp
#from array import array
import numpy as np
##from pylab import *
from matplotlib import pyplot as plt

valuesfile=open('Data/bp_ptt_abhi2.txt','r',1)
data=[]
data1=[]
Fs=500#sampling frequency in Hz, sampling interval=2ms

for value in valuesfile:
    #print value
    if value is '':
        break
    a= value.split(' ')
    if a[0] is '' or a[1] is '':break
    sensor=int(a[0])
    sensor1=int(a[1])
    data.append(sensor)
    data1.append(sensor1)

length=len(data)
print "Length:", length

wave=thinkdsp.Wave(ys=data,framerate=Fs)
wave1=thinkdsp.Wave(ys=data1,framerate=Fs)


plt.subplot(211)
wave.plot()
plt.xlabel("Time(sec)")
plt.title("Reflective Wrist Pulse Wave")
plt.ylabel("Pulse Amplitude")
plt.grid()
plt.subplots_adjust(hspace=.5)

plt.subplot(212)
wave1.plot()
plt.title("Finger Pulse Wave")
plt.xlabel("Time(sec)")
plt.ylabel("Pulse Amplitude")
plt.grid()
plt.show()

