import thinkdsp
import adaptfilt as adf
import numpy as np
from matplotlib import pyplot as plt
import itertools
from scipy import signal

valuesfile=open('Data/abhishek_SpO2_240ms_new.txt','rU',1)

data=[]
data1=[]
ref=[]
Fs=4.17#500#sampling frequency in Hz, sampling interval=2ms

for value in valuesfile:
    #print value
    if value is '':
        break
    a= value.split(' ')
    if a[0] is '' or a[1] is '':break
    sensor=int(a[0])
    sensor1=int(a[1])
    ref.append(sensor1-sensor)
    data.append(sensor)
    data1.append(sensor1)

length=len(data)
print "Length:", length

y,e,w=adf.nlms(ref,data,5,1)


wave=thinkdsp.Wave(ys=data1,framerate=Fs)
wave1=thinkdsp.Wave(ys=data,framerate=Fs)
wave2=thinkdsp.Wave(ys=y,framerate=Fs)

spectrum=wave.make_spectrum()
spectrum1=wave1.make_spectrum()
spectrum2=wave2.make_spectrum()


##
##spectrum.low_pass(cutoff=1.5, factor=0)
##spectrum.high_pass(cutoff=1, factor=0)
##
##
##spectrum1.low_pass(cutoff=1.5, factor=0)
##spectrum1.high_pass(cutoff=1, factor=0)
##
##wave_fltr=spectrum.make_wave()
##wave1_fltr=spectrum1.make_wave()
##
##
plt.subplot(321)
wave.plot()
plt.xlabel("Time(sec)")
plt.title("Reflective Wrist Pulse Wave")
plt.ylabel("Pulse Amplitude")
plt.grid()

plt.subplots_adjust(hspace=.5)

plt.subplot(323)
wave1.plot()
plt.xlabel("Time(sec)")
plt.title("Finger Pulse Wave")
plt.ylabel("Pulse Amplitude")


plt.subplot(322)
spectrum.plot()
plt.title("Magnitude Spectrum")
plt.xlabel("Frequency(Hz)")
plt.ylabel("Magnitude")
plt.xlim(0,5)

plt.subplot(324)
spectrum1.plot()
plt.title("Magnitude Spectrum")
plt.xlabel("Frequency(Hz)")
plt.ylabel("Magnitude")
##plt.xlim(0,5)

plt.subplot(325)
wave2.plot()
plt.xlabel("Time(sec)")
plt.title("Reflective Wrist Pulse Wave")
plt.ylabel("Pulse Amplitude")
plt.grid()

plt.subplots_adjust(hspace=.5)

plt.subplot(326)
spectrum2.plot()
plt.xlabel("Time(sec)")
plt.title("Finger Pulse Wave")
plt.ylabel("Pulse Amplitude")


plt.show()
##plt.subplot(233)
##wave_fltr.plot()
##plt.title("Reflective Wrist Pulse Wave--Filtered")
##plt.xlabel("Time(sec)")
##plt.grid()
##plt.ylabel("Pulse Amplitude")
##
##plt.subplot(236)
##wave1_fltr.plot()
##plt.xlabel("Time(sec)")
##plt.title("Finger Pulse Wave--Filtered")
##plt.grid()
##plt.ylabel("Pulse Amplitude")
##
##plt.show()
##
##
