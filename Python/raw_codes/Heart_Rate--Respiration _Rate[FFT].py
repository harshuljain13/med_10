import thinkdsp
#from array import array
import numpy as np
##from pylab import *
from matplotlib import pyplot as plt

valuesfile=open('Data/abhishek_new_sensor_cap.txt','r',1)
data=[]
Fs=12.5#sampling frequency in Hz, sampling interval=80 ms

for value in valuesfile:
    #print value
    if value is '':
        break
    sensor=int(value)
    data.append(sensor)

length=len(data)
print "Length:", length

wave=thinkdsp.Wave(ys=data,framerate=Fs)
spectrum=wave.make_spectrum()
spectrum_heart=wave.make_spectrum()
spectrum_resp=wave.make_spectrum()

fft_mag=list(np.absolute(spectrum.hs))
fft_length= len(fft_mag)

spectrum_heart.high_pass(cutoff=0.5,factor=0.001)
spectrum_heart.low_pass(cutoff=4,factor=0.001)
fft_heart=list(np.absolute(spectrum_heart.hs))

max_fft_heart=max(fft_heart)
heart_sample=fft_heart.index(max_fft_heart)
hr=heart_sample*Fs/length*60
print "Heart Rate:", hr, "BPM"

spectrum_resp.high_pass(cutoff=0.15,factor=0)
spectrum_resp.low_pass(cutoff=0.5,factor=0)
fft_resp=list(np.absolute(spectrum_resp.hs))

max_fft_resp=max(fft_resp)
resp_sample=fft_resp.index(max_fft_resp)
rr=resp_sample*Fs/length*60
print "Respiration Rate:", rr, "RPM"

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
plt.ylim(0,max(max_fft_heart,max_fft_resp)+500)
plt.xlim(0,3)
plt.title("Magnitude Spectrum")
plt.xlabel("Frequency(Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.show()

