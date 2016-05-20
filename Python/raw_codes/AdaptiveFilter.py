import thinkdsp
#from array import array
import numpy as np
##from pylab import *
from matplotlib import pyplot as plt

valuesfile=open('Data/abhishek_SpO2_240ms_new.txt','r',1)
data=[]
Fs=12.5#sampling frequency in Hz, sampling interval=80 ms

for value in valuesfile:
    #print value
    if value is '':
        break
    a= value.split(' ')
    analog_red=int(a[0])
    analog_ir=int(a[1])
    data.append(analog_ir)

length=len(data)
print "Length:", length

wave=thinkdsp.Wave(ys=data,framerate=Fs)
spectrum=wave.make_spectrum()

plt.subplot(211)
wave.plot()
##plt.xlim(20,60)
plt.xlabel("Time(sec)")
plt.title("Pulse Wave")
plt.ylabel("Pulse Amplitude")
plt.grid()
plt.subplots_adjust(hspace=.5)

plt.subplot(212)
spectrum.plot()
plt.xlim(0,3)
plt.title("Magnitude Spectrum")
plt.xlabel("Frequency(Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.show()
