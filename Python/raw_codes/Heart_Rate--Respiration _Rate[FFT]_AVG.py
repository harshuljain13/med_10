import thinkdsp
#from array import array
import numpy as np
##from pylab import *
from matplotlib import pyplot as plt

valuesfile=open('abhishek_new_sensor_short2.txt','r',1)
data=[]
Fs=12.5#sampling frequency in Hz

for value in valuesfile:
    #print value
    if value is '':
        break
    value=1023-int(value)
    data.append(value)

length=len(data)
##print "Length:", length

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
thresh_resp=max_fft_heart/4
thresh_heart=max_fft_heart*2/3


weight=0
fft_weighted_sum=0

for i in range(0,fft_length):
    if fft_heart[i] >= thresh_heart:
        weight+=fft_heart[i]
        fft_weighted_sum+=fft_heart[i]*i


heart_sample=fft_weighted_sum/weight
hr=heart_sample*Fs/length*60
print "Heart Rate:", hr, "BPM"

spectrum_resp.high_pass(cutoff=0.15,factor=0)
spectrum_resp.low_pass(cutoff=0.5,factor=0)
fft_resp=list(np.absolute(spectrum_resp.hs))

weight=0
fft_weighted_sum=0

for i in range(0,fft_length):
    if fft_resp[i] >= thresh_resp:
        weight+=fft_resp[i]
        fft_weighted_sum+=fft_resp[i]*i

resp_sample=fft_weighted_sum/weight
rr=resp_sample*Fs/length*60
print "Respiration Rate:", rr, "RPM"

plt.subplot(211)
wave.plot()
plt.xlim(20,60)
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.grid()

plt.subplot(212)
spectrum.plot()
plt.ylim(0,max_fft_heart)
plt.xlim(0,3)
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.grid()
plt.show()
