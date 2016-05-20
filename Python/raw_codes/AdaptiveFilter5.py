import thinkdsp
import adaptfilt as adf
import numpy as np
from matplotlib import pyplot as plt
import itertools
from scipy import signal

valuesfile=open('Data/abhishek_SpO2_240ms.txt','rU',1)

data=[]
data1=[]
data2=[]
ref=[]
sas=[]
nT=4

Fs=4.17#500#sampling frequency in Hz, sampling interval=2ms

for value in valuesfile:
    #print value
    if value is '':
        break
    a= value.split(' ')
    if a[0] is '' or a[1] is '':break
    sensor=float(a[0])
    sensor1=float(a[1])
    ref.append(sensor1-sensor)
    data.append(sensor)
    data1.append(sensor1)



x1,e1,w1=adf.nlms(ref,data,5,1)
x2,e2,w2=adf.nlms(ref,data1,5,1)

length=len(x1)
print "Length:", length

ex1s=.0
ex2s=.0
ex1x2=.0
esdx1=.0
esdx2=.0
ess=.0
esds=.0
essd=.0
rv=0.9
alpha=.0
beta=[]
for i in range(0,20):
    sas.append(x1[i]-rv*x2[i])
##    ex1s=(ex1s*i+data[i]**2)/(i+1)
##    ex2s=(ex2s*i+data1[i]**2)/(i+1)
##    ess=(ess*i+sas[i]**2)/(i+1)
##    esdx1=(esdx1*i+data[i]*sas[i])/(i+1)
##    esdx2=(esdx2*i+data1[i]*sas[i])/(i+1)
##    ex1x2=(ex1x2*i+data[i]*data1[i])/(i+1)

for i in range(0,20-nT):
    esds=(esds*i+sas[i]**2)/(i+1)               ##estimate of s_delay squared
    essd=(essd*i+sas[i]*sas[i+nT])/(i+1)        ##estimate of s_delay*sas

    ex1s=(ex1s*i+x1[i+nT]**2)/(i+1)           ##estimate of x1 squared
    ex2s=(ex2s*i+x2[i+nT]**2)/(i+1)          ##estimate of x2 squared
    ex1x2=(ex1x2*i+x1[i+nT]*x2[i+nT])/(i+1)   ##estimate of x1*x2
    ess=(ess*i+sas[i+nT]**2)/(i+1)              ##estimate of sas squared
    esdx1=(esdx1*i+x1[i+nT]*sas[i])/(i+1)     ##estimate of s_delay*x1
    esdx2=(esdx2*i+x2[i+nT]*sas[i])/(i+1)    ##estimate of s_delay*x2


print ex1s,ex2s,ex1x2,esdx1,esdx2,ess,esds,essd    
for i in range(20,length):
    sas.append(x1[i]-rv*x2[i])
    ex1s=(ex1s*i+x1[i]**2)/(i+1)
    ex2s=(ex2s*i+x2[i]**2)/(i+1)
    ess=(ess*i+sas[i]**2)/(i+1)
    esdx1=(esdx1*i+x1[i]*sas[i-nT])/(i+1)
    esdx2=(esdx2*i+x2[i]*sas[i-nT])/(i+1)
    ex1x2=(ex1x2*i+x1[i]*x2[i])/(i+1)
    esds=(esds*i+sas[i-nT]**2)/(i+1)
    essd=(essd*i+sas[i]*sas[i-nT])/(i+1)

    rv = (ex1x2*esdx1 - ex1s*esdx2)/(ex2s*esdx1 - ex1x2*esdx2)
    b = essd/esds

    alpha = (ex1s-rv*ex1x2)/ess
    beta.append((rv*alpha)/(1-alpha))
    
##    print "rv:" , rv, "beta",beta,"alpha", alpha
print "beta length: ", len(beta)
venous_ref=[]
for i in range(0,len(beta)-4):
    venous_ref.append(x1[20+i]- beta[i]*x2[20+i])

print "venous_ref length: ", len(venous_ref)
    
xf1,ef1,wf1=adf.nlms(x1[20:-4],venous_ref,5,1)

print "length of ef1: ", len(ef1)

data2= data2 + list(ef1)
print data2


wave=thinkdsp.Wave(ys=data2,framerate=Fs)
##wave1=thinkdsp.Wave(ys=data,framerate=Fs)
##wave2=thinkdsp.Wave(ys=x1,framerate=Fs)
##
spectrum=wave.make_spectrum()
##spectrum1=wave1.make_spectrum()
##spectrum2=wave2.make_spectrum()
##
##
####
####spectrum.low_pass(cutoff=1.5, factor=0)
####spectrum.high_pass(cutoff=1, factor=0)
####
####
####spectrum1.low_pass(cutoff=1.5, factor=0)
####spectrum1.high_pass(cutoff=1, factor=0)
####
####wave_fltr=spectrum.make_wave()
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

##
##plt.subplot(324)
##spectrum1.plot()
##plt.title("Magnitude Spectrum")
##plt.xlabel("Frequency(Hz)")
##plt.ylabel("Magnitude")
####plt.xlim(0,5)
##
##plt.subplot(325)
##wave2.plot()
##plt.xlabel("Time(sec)")
##plt.title("Reflective Wrist Pulse Wave")
##plt.ylabel("Pulse Amplitude")
##plt.grid()
##
##plt.subplots_adjust(hspace=.5)
##
##plt.subplot(326)
##spectrum2.plot()
##plt.xlabel("Time(sec)")
##plt.title("Finger Pulse Wave")
##plt.ylabel("Pulse Amplitude")
##
##
##plt.show()
####plt.subplot(233)
####wave_fltr.plot()
####plt.title("Reflective Wrist Pulse Wave--Filtered")
####plt.xlabel("Time(sec)")
####plt.grid()
####plt.ylabel("Pulse Amplitude")
####
####plt.subplot(236)
####wave1_fltr.plot()
####plt.xlabel("Time(sec)")
####plt.title("Finger Pulse Wave--Filtered")
####plt.grid()
####plt.ylabel("Pulse Amplitude")
####
####plt.show()
####
####
