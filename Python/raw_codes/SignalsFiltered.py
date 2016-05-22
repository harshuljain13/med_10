import thinkdsp
import numpy as np
from matplotlib import pyplot as plt
import itertools
from scipy import signal

valuesfile=open('Data/patients/1.txt','r',1)
##file1=open("Data/bp_ptt_abhi-forearm_again_filtered1.txt",'ab',1);

data=[]
data1=[]
Fs=62.5#4.17#500#sampling frequency in Hz, sampling interval=2ms

##while time<10:
##    value=valuesfile.readline()


while True:
    value=valuesfile.readline()
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


##print ptt.index(max(ptt))

wave=thinkdsp.Wave(ys=data,framerate=Fs)
wave1=thinkdsp.Wave(ys=data1,framerate=Fs)

spectrum=wave.make_spectrum()
spectrum1=wave1.make_spectrum()


##spectrum.low_pass(cutoff=1.5, factor=0)
##spectrum.high_pass(cutoff=1, factor=0)
##
##
##spectrum1.low_pass(cutoff=1.5, factor=0)
##spectrum1.high_pass(cutoff=1, factor=0)

wave_fltr=spectrum.make_wave()
wave1_fltr=spectrum1.make_wave()

##ptt=signal.correlate(wave1.ys,wave.ys,mode='full')/128
##print signal.argrelextrema(np.array(wave_fltr.ys),np.less)
##print signal.argrelextrema(np.array(wave1_fltr.ys),np.less)

##ptt=signal.correlate(wave1_fltr.ys,wave_fltr.ys,mode='full')/128
##bp_max=np.argmax(ptt)
##print bp_max
##print "PTT: ", (length-bp_max)


##for i,j in itertools.izip(wave_fltr.ys, wave1_fltr.ys):
##    file1.write(str(int(i))+' '+str(int(j))+'\r\n')

plt.subplot(231)
wave.plot()
plt.xlabel("Time(sec)")
plt.title("Reflective Wrist Pulse Wave")
plt.ylabel("Pulse Amplitude")
plt.grid()
plt.subplots_adjust(hspace=.5)

plt.subplot(234)
wave1.plot()
plt.xlabel("Time(sec)")
plt.title("Finger Pulse Wave")
plt.ylabel("Pulse Amplitude")

plt.subplot(232)
spectrum.plot()
plt.title("Magnitude Spectrum")
plt.xlabel("Frequency(Hz)")
plt.ylabel("Magnitude")
plt.xlim(0,5)

plt.subplot(235)
spectrum1.plot()
plt.title("Magnitude Spectrum")
plt.xlabel("Frequency(Hz)")
plt.ylabel("Magnitude")
plt.xlim(0,5)

plt.subplot(233)
wave_fltr.plot()
plt.title("Reflective Wrist Pulse Wave--Filtered")
plt.xlabel("Time(sec)")
plt.grid()
plt.ylabel("Pulse Amplitude")

plt.subplot(236)
wave1_fltr.plot()
plt.xlabel("Time(sec)")
plt.title("Finger Pulse Wave--Filtered")
plt.grid()
plt.ylabel("Pulse Amplitude")

plt.show()


