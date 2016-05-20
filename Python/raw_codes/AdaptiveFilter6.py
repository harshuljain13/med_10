import thinkdsp
import adaptfilt as adf
import numpy as np
from matplotlib import pyplot as plt
import sys

valuesfile=open('Python/Data/ujjawal_4ms_spo2_1.txt','r',1)
##file1=open('Python/Data/shobhit_spo2_motion1_mono.txt.txt','w',1);
data=[]
data1=[]
data2=[]
ref=[]
sas=[]
sdelay=[]
##nT=5              ##samples in one time period
Fs=250           #500#sampling frequency in Hz, sampling interval=2ms
window=int(6*Fs)          ##samples per Beta
boundary=window-1 ##correction for division

for value in valuesfile:
    #print value
    if value is '':
        break
    a= value.split(' ')
    if a[0] is '' or a[1] is '':break
##    file1.write(a[0])
    sensor=float(a[0])
    sensor1=float(a[1])
    
##    file1.write('\n')
    if(sensor>150 and sensor<762 and sensor1>150 and sensor1<762):
        ref.append(sensor1-sensor)
        data.append(sensor)
        data1.append(sensor1)

length=len(data)
print "Length:", length

def butter_highpass(interval, sampling_rate, cutoff, order=5):
    nyq = sampling_rate * 0.5

    stopfreq = float(cutoff)
    cornerfreq = 0.4 * stopfreq  # (?)

    ws = cornerfreq/nyq
    wp = stopfreq/nyq

    # for bandpass:
    # wp = [0.2, 0.5], ws = [0.1, 0.6]

    N, wn = scipy.signal.buttord(wp, ws, 3, 16)   # (?)

    # for hardcoded order:
    # N = order

    b, a = scipy.signal.butter(N, wn, btype='high')   # should 'high' be here for bandpass?
    sf = scipy.signal.lfilter(b, a, interval)
    return sf

## calculating fundamental time period of input original signal

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
fund_freq=heart_sample*Fs/length*60
nT=int(fund_freq/60)*Fs
print "Fundamental frequency from original data :", fund_freq,'BPM','nT = ',nT

spectrum_resp.high_pass(cutoff=0.15,factor=0)
spectrum_resp.low_pass(cutoff=0.5,factor=0)
fft_resp=list(np.absolute(spectrum_resp.hs))

max_fft_resp=max(fft_resp)
resp_sample=fft_resp.index(max_fft_resp)
rr=resp_sample*Fs/length*60
print "Respiration Rate without filtering :", rr, "RPM"

## FIRST ADAPTIVE FILTER
x1,e1,w1=adf.nlms(ref,data,11,1)
x2,e2,w2=adf.nlms(ref,data1,11,1)

## calculating fundamental time period of input signal x1
length=len(x1)
print 'length of x1 is' , length
wave=thinkdsp.Wave(ys=x1,framerate=Fs)
spectrum=wave.make_spectrum()
spectrum_heart=wave.make_spectrum()
spectrum_resp=wave.make_spectrum()

fft_mag=list(np.absolute(spectrum.hs))
fft_length= len(fft_mag)

spectrum_heart.high_pass(cutoff=0.7,factor=0.001)
spectrum_heart.low_pass(cutoff=4,factor=0.001)
fft_heart=list(np.absolute(spectrum_heart.hs))

max_fft_heart=max(fft_heart)
heart_sample=fft_heart.index(max_fft_heart)
fund_freq=heart_sample*Fs/length*60
nT=int(fund_freq/60*Fs)
print "Heart Rate after first filter :", fund_freq,'BPM','nT = ',nT

spectrum_resp.high_pass(cutoff=0.15,factor=0)
spectrum_resp.low_pass(cutoff=0.4,factor=0)
fft_resp=list(np.absolute(spectrum_resp.hs))

max_fft_resp=max(fft_resp)
resp_sample=fft_resp.index(max_fft_resp)
rr=resp_sample*Fs/length*60
print "Respiration Rate after first filter:", rr, "RPM"

##Second Filter algorithm

ex1s=.0
ex2s=.0
ex1x2=.0
esas=.0
esdx1=.0
esdx2=.0
ess=.0
esds=.0
essd=.0
rv=.8
alpha=.0
beta=[]

## calculating first/initial rv
for i in range(0,2*nT):
##    print x1[i],x2[i]
    sas.append(x1[i]-rv*x2[i])  ##getting values of sas till nT for sdelay
##    print 'sas =', sas
    ex1s=(ex1s*i+x1[i]**2)/(i+1)
    ex2s=(ex2s*i+x2[i]**2)/(i+1)
    ess=(ess*i+sas[i]**2)/(i+1)
    esdx1=(esdx1*i+x1[i]*sas[i])/(i+1)
    esdx2=(esdx2*i+x2[i]*sas[i])/(i+1)
    ex1x2=(ex1x2*i+x1[i]*x2[i])/(i+1)
    if((ex2s*esdx1 - ex1x2*esdx2)):
        rv = (ex1x2*esdx1 - ex1s*esdx2)/(ex2s*esdx1 - ex1x2*esdx2)    
##    print esdx1,ex2s,esdx1,ex1x2,esdx2
##    print (ex2s*esdx1 - ex1x2*esdx2),rv

##calculating rv,alpha and updating beta every 20 samples
for i in range(2*nT,length-(window-1)):
    for j in range(0,window):    
        sas.append(x1[i]-rv*x2[i])
        ex1s=(ex1s*j+x1[i]**2)/(j+1)
        ex2s=(ex2s*j+x2[i]**2)/(j+1)
        ess=(ess*j+sas[i]**2)/(j+1)
        esdx1=(esdx1*j+x1[i]*sas[i-nT])/(j+1)
        esdx2=(esdx2*j+x2[i]*sas[i-nT])/(j+1)
        ex1x2=(ex1x2*j+x1[i]*x2[i])/(j+1)
    ##        esds=(esds*j+sas[i-nT]**2)/(j+1)
    ##        essd=(essd*j+sas[i]*sas[i-nT])/(j+1)
        i=i+1
        
    if((ex2s*esdx1 - ex1x2*esdx2)):
        rv = (ex1x2*esdx1 - ex1s*esdx2)/(ex2s*esdx1 - ex1x2*esdx2)
    ##  b = essd/esds
    alpha = (ex1s-rv*ex1x2)/ess
    for j in range(0,window):
        beta.append((rv*alpha)/(1-alpha))
##    print beta
    i=i-1

##reference filter signal for secons filter
venous_ref=[]
for i in range(0,length-3*nT):
    venous_ref.append(x1[2*nT+i]- beta[i]*x2[2*nT+i])

    
xf1,ef1,wf1=adf.nlms(venous_ref,x2[2*nT:],11,1)

data2= data2 + list(xf1)


##print data2

length=len(data2)
print 'length of data2 is' , length
wave=thinkdsp.Wave(ys=data2,framerate=Fs)
spectrum=wave.make_spectrum()
spectrum_heart=wave.make_spectrum()
spectrum_resp=wave.make_spectrum()

fft_mag=list(np.absolute(spectrum.hs))
fft_length= len(fft_mag)

spectrum_heart.high_pass(cutoff=0.7,factor=0.001)
spectrum_heart.low_pass(cutoff=4,factor=0.001)
fft_heart=list(np.absolute(spectrum_heart.hs))

max_fft_heart=max(fft_heart)
heart_sample=fft_heart.index(max_fft_heart)
fund_freq=(heart_sample*Fs/length)*60
nT=int(fund_freq/60*Fs)
print "Fundamental frequency after second filter :", fund_freq,'BPM','nT = ',nT

spectrum_resp.high_pass(cutoff=0.15,factor=0)
spectrum_resp.low_pass(cutoff=0.4,factor=0)
fft_resp=list(np.absolute(spectrum_resp.hs))

max_fft_resp=max(fft_resp)
resp_sample=fft_resp.index(max_fft_resp)
rr=resp_sample*Fs/length*60
print "Respiration Rate after second filter:", rr, "RPM"

##spectrum1=wave1.make_spectrum()
##spectrum2=wave2.make_spectrum()
##
##
####
##spectrum.low_pass(cutoff=3, factor=0)
##spectrum.high_pass(cutoff=.5, factor=0)
####
####
####spectrum1.low_pass(cutoff=1.5, factor=0)
####spectrum1.high_pass(cutoff=1, factor=0)
####    
wave_fltr=spectrum.make_wave()
####wave1_fltr=spectrum1.make_wave()
####
####
plt.subplot(211)
wave.plot()
plt.xlabel("Time(sec)")
plt.title("Reflective Wrist Pulse Wave")
plt.ylabel("Pulse Amplitude")
plt.grid()

plt.subplots_adjust(hspace=.5)

##plt.subplot(323)
##wave1.plot()
##plt.xlabel("Time(sec)")
##plt.title("Finger Pulse Wave")
##plt.ylabel("Pulse Amplitude")
##
##
plt.subplot(212)
spectrum.plot()
plt.title("Magnitude Spectrum")
plt.xlabel("Frequency(Hz)")
plt.ylabel("Magnitude")
plt.xlim(0,5)
plt.show()

