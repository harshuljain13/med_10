import serial
import numpy as np
from array import array
from matplotlib import pyplot as plt
import pylab as pl
import math
import cmath
from multiprocessing import Process
import thinkdsp
import adaptfilt as adf
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import pickle
import scipy as sp
import pandas as pd
import csv as csv
from sklearn.ensemble import RandomForestClassifier
import os

# training forest

ftrain_input = []
ftrain_output = []
Ftrainer_in = open('RndFrstInputTrain.txt', 'r', 1)
Ftrainer_out = open('RndFrstOutputTrain.txt', 'r', 1)
for value2 in Ftrainer_out:
    ftrain_output.append(float(value2))
for value1 in Ftrainer_in:
    if value1 is '':
        break
    xtu = value1.split("	")
    xlu = [xtu[0], xtu[1], xtu[2], xtu[3], xtu[4], xtu[5], xtu[6], xtu[7]]
    ftrain_input.append(xlu)

forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit(ftrain_input, ftrain_output)

##x = np.linspace(0, 4*np.pi, 100)
ds = SupervisedDataSet(11, 2)

# This is where the input for neural network training goes
ltrain_input = []
ltrain_output = []
Ltrainer_in = open('NuInputTrainx.txt', 'r', 1)
Ltrainer_out = open('NuOutputTrainx.txt', 'r', 1)
for value1 in Ltrainer_in:
    xtu = value1.split("	")
    for value2 in Ltrainer_out:
        ##while True:
        ##value1=Ltrainer_in.readline()
        ##value2=Ltrainer_out.readline()
        ##if value1 is '' or value2 is '':
        ##    break
        ##xtu=value1.split("	")
        xbu = value2.split("	")
        xlu = [xtu[0], xtu[1], xtu[2], xtu[3], xtu[4], xtu[5], xtu[6], xtu[7], xtu[8], xtu[9], xtu[10]]
        xvu = [xbu[0], xbu[1]]
        ltrain_input.append(xlu)
        ltrain_output.append(xvu)
        ds.addSample(xlu, xvu)

##for i in x:
##    ds.addSample(i,50*math.sin(i))
##print ds

n = buildNetwork(ds.indim, 40, ds.outdim, recurrent=True)
t = BackpropTrainer(n, learningrate=0.05, momentum=0.5, verbose=True)
t.trainUntilConvergence(ds, 10, continueEpochs=10, validationProportion=0.01)
t.testOnData(verbose=True)

fileObject = open('trained_net', 'w')
pickle.dump(n, fileObject)
fileObject.close()

N1 = 3111
L = 10
j = 1
T = 0.08
##N=100
##y=np.empty(100)
x = np.empty(100)
qw = 0


##yn=np.empty(100)

def parameter(y, yn, ref):
    os.system('CLS')
    htbt, rrt = estimate(y, yn, ref)
    L = 10
    j = 1
    T = 0.08
    ##N=100
    ##y=np.empty(100)
    N = len(y)
    for cntr in range(1, N):
        # x[cntr-1]=cntr
        # y[cntr-1]=1*math.sin(314.1416*cntr*T)+3*math.sin(2*314.1416*cntr*T)
        # yn[cntr-1]=1*math.sin(314.1416*cntr*T-1)+3*math.sin(2*314.1416*cntr*T-1)
        suom = 0
        sumi = 0
        acsum = 0
        acsum1 = 0

    for cntr in range(1, N):
        suom = suom + y[cntr - 1]
        acsum = acsum + y[cntr - 1] * y[cntr - 1]
        sumi = sumi + yn[cntr - 1]
        acsum1 = acsum1 + yn[cntr - 1] * yn[cntr - 1]
    avg = suom / N
    avg1 = sumi / N
    ac = math.sqrt(acsum / N)
    ac1 = math.sqrt(acsum1 / N)
    spO2 = (ac / avg) / (ac1 / avg1)
    for cntr in range(1, N):
        y[cntr - 1] = y[cntr - 1] - avg
        yn[cntr - 1] = yn[cntr - 1] - avg1
    d = np.empty(N - L)
    j = 1
    for cntr in range(L, N):
        d[j - 1] = y[cntr]
        j = j + 1
    # formation of D
    D = np.empty([N - L, L])
    r = 1
    c = 1
    for cntr in range(1, N - L + 1):
        for cntr1 in range(1, L + 1):
            D[r - 1, c - 1] = y[L - cntr1 + cntr - 1]
            c = c + 1
        c = 1
        r = r + 1

    inversa = np.linalg.pinv(D)
    a = np.empty(L)
    a = np.dot(inversa, d)
    # obtaining z roots
    z = np.empty(11)
    for cntr in range(0, 11):
        if cntr == 0:
            z[cntr] = 1
        else:
            z[cntr] = -a[cntr - 1]
    rots = np.roots(z)

    # formation of y=uc and y=y1
    y1 = np.empty(L)
    for cntr in range(0, L):
        y1[cntr] = y[L + cntr - 1]

    u = np.empty([L, L], complex)
    c1 = np.empty(L)

    r = 1
    c = 1
    for cntr in range(1, L + 1):
        for cntr1 in range(1, L + 1):
            u[r - 1, c - 1] = u[r - 1, c - 1] + 0j
            u[r - 1, c - 1] = pow(rots[cntr1 - 1], r - 1)
            c = c + 1
        c = 1
        r = r + 1

    c1 = np.dot(np.linalg.pinv(u), y1)
    # amplitude

    val = np.empty(L)
    for cntr in range(0, L - 1):
        val[cntr] = abs(c1[cntr] * 2)
    # frequency
    f = np.empty(L)
    for cntr in range(0, L - 1):
        re = rots[cntr].real
        im = rots[cntr].imag
        kk = 2 * 3.1416 * T
        if re != 0:
            f[cntr] = math.atan(im / re) / kk

    phi = np.empty(L)
    for cntr in range(0, L):
        # print c1[cntr].real , c1[cntr].imag
        if c1[cntr].real == 0:
            phi[cntr] = cmath.pi / 2
        else:
            real = c1[cntr].imag
            imaginary = c1[cntr].real
            if real != 0:
                phi[cntr] = math.atan(imaginary / real)
            else:
                phi[cntr] = 0
                val[cntr] = 0
                f[cntr] = 0
    for cntr in range(0, L):
        if f[cntr] < 0.2 or val[cntr] < 0.01:
            val[cntr] = 0
            phi[cntr] = 0
            f[cntr] = 0
    val = [x for (y, x) in sorted(zip(f, val))]
    phi = [x for (y, x) in sorted(zip(f, phi))]
    f = sorted(f)
    for cntr in range(0, 9):
        if f[cntr] != 0:
            ##            print val[cntr],'   ',f[cntr],'   ',phi[cntr],'   '
            xx = str(val[cntr]) + ' ' + str(f[cntr]) + ' ' + str(avg) + ' ' + str(avg1) + ' ' + str(spO2) + ' '
        ##    print '\n'
        ##    print avg,'   ',avg1,'   ',spO2,'  '
        ##    print '\n'
    fk = open("outputparams.txt", 'a', 1)
    fk.write("\n")
    fk.write(xx)
    fk.close()
    ## getting neural trained data
    fileObject = open('trained_net', 'r')
    net = pickle.load(fileObject)
    ##    qw=0
    ##    qw=qw+0.1
    # printing neural resultsavg1
    ##    print f[9]
    ##    clear = "\n" * 100
    ##    print clear

    pout = [ f[9], f[8], f[7], f[6], f[5], val[9], val[8], val[7], val[6], val[5], avg ]
    print pout
    bp1 = str(net.activate(pout)).split()
    print "Blood Pressure [normal diastolic < 80, systolic < 140] : " + str(bp1[1]) + " " + str(bp1[2])
    # printing forest results
    age = 21
    sex = 1
    BMI = 20
    minet = 120
    test_data = [avg, avg1, spO2, age, sex, BMI, minet, htbt]
    output = forest.predict(test_data)

    print "Glucose level[before eating 70-90 after eating < 140]  : " + str(output) + ' '

    wow = 110 - 15 * spO2

    print "Oxygen Saturation [normal > 94]                        : " + str(wow)

    return htbt, rrt, bp1, str(output), str(wow)


##................................................................##

def estimate(y, y1, ref1):
    data2 = []
    sas = []
    sdelay = []
    ##nT=5                  ##samples in one time period
    Fs = 62.5  # 500#sampling frequency in Hz, sampling interval=2ms
    ##    window=int(Fs)        ##samples per Beta
    window = 30
    order = 10
    boundary = window - 1  ##correction for dividion
    length = len(y)
    wave = thinkdsp.Wave(ys=y, framerate=Fs)
    spectrum = wave.make_spectrum()
    spectrum_heart = wave.make_spectrum()
    spectrum_resp = wave.make_spectrum()

    fft_mag = list(np.absolute(spectrum.hs))
    fft_length = len(fft_mag)

    spectrum_heart.high_pass(cutoff=0.5, factor=0.001)
    spectrum_heart.low_pass(cutoff=4, factor=0.001)
    fft_heart = list(np.absolute(spectrum_heart.hs))
    spectrum_resp.high_pass(cutoff=0.15, factor=0)
    spectrum_resp.low_pass(cutoff=0.4, factor=0)
    fft_resp = list(np.absolute(spectrum_resp.hs))

    max_fft_heart = max(fft_heart)
    heart_sample = fft_heart.index(max_fft_heart)
    fund_freq = heart_sample * Fs / length * 60
    ##    fund_freq-=0.2*fund_freq
    nT = int(fund_freq / 60 * Fs)
    max_fft_resp = max(fft_resp)
    resp_sample = fft_resp.index(max_fft_resp)
    rr = resp_sample * Fs / length * 60

    ## FIRST ADAPTIVE FILTER
    x1, e1, w1 = adf.nlms(ref1, y, order, 1)
    x2, e2, w2 = adf.nlms(ref1, y1, order, 1)

    ## calculating fundamental time period of input signal x1
    length = len(x1)
    wave = thinkdsp.Wave(ys=x1, framerate=Fs)
    spectrum = wave.make_spectrum()
    spectrum_heart = wave.make_spectrum()
    spectrum_resp = wave.make_spectrum()

    fft_mag = list(np.absolute(spectrum.hs))
    fft_length = len(fft_mag)

    spectrum_heart.high_pass(cutoff=0.5, factor=0.001)
    spectrum_heart.low_pass(cutoff=4, factor=0.001)
    fft_heart = list(np.absolute(spectrum_heart.hs))
    spectrum_resp.high_pass(cutoff=0.15, factor=0)
    spectrum_resp.low_pass(cutoff=0.4, factor=0)
    fft_resp = list(np.absolute(spectrum_resp.hs))

    max_fft_heart = max(fft_heart)
    heart_sample = fft_heart.index(max_fft_heart)
    fund_freq = heart_sample * Fs / length * 60
    nT = int(fund_freq / 60 * Fs)
    max_fft_resp = max(fft_resp)
    resp_sample = fft_resp.index(max_fft_resp)
    rr = resp_sample * Fs / length * 60

    ##Second Filter algorithm

    ex1s = .0
    ex2s = .0
    ex1x2 = .0
    esas = .0
    esdx1 = .0
    esdx2 = .0
    ess = .0
    esds = .0
    essd = .0
    rv = .8
    alpha = .0
    beta = []
    length = length - length % window
    ## calculating first/initial rv
    for i in range(0, nT):
        sas.append(x1[i] - rv * x2[i])  ##getting values of sas till nT for sdelay
        ex1s = (ex1s * i + x1[i] ** 2) / (i + 1)
        ex2s = (ex2s * i + x2[i] ** 2) / (i + 1)
        ess = (ess * i + sas[i] ** 2) / (i + 1)
        esdx1 = (esdx1 * i + x1[i] * sas[i]) / (i + 1)
        esdx2 = (esdx2 * i + x2[i] * sas[i]) / (i + 1)
        ex1x2 = (ex1x2 * i + x1[i] * x2[i]) / (i + 1)
        if ((ex2s * esdx1 - ex1x2 * esdx2)):
            rv = (ex1x2 * esdx1 - ex1s * esdx2) / (ex2s * esdx1 - ex1x2 * esdx2)
            ##    print esdx1,ex2s,esdx1,ex1x2,esdx2
    ##    print (ex2s*esdx1 - ex1x2*esdx2),rv

    ##calculating rv,alpha and updating beta every 20 samples
    for i in range(nT, length - window):
        for j in range(0, window):
            sas.append(x1[i] - rv * x2[i])
            ex1s = (ex1s * j + x1[i] ** 2) / (j + 1)
            ex2s = (ex2s * j + x2[i] ** 2) / (j + 1)
            ess = (ess * j + sas[i] ** 2) / (j + 1)
            esdx1 = (esdx1 * j + x1[i] * sas[i - nT]) / (j + 1)
            esdx2 = (esdx2 * j + x2[i] * sas[i - nT]) / (j + 1)
            ex1x2 = (ex1x2 * j + x1[i] * x2[i]) / (j + 1)
            ##        esds=(esds*j+sas[i-nT]**2)/(j+1)
            ##        essd=(essd*j+sas[i]*sas[i-nT])/(j+1)
            i = i + 1

        if ((ex2s * esdx1 - ex1x2 * esdx2)):
            rv = (ex1x2 * esdx1 - ex1s * esdx2) / (ex2s * esdx1 - ex1x2 * esdx2)
        ##  b = essd/esds
        alpha = (ex1s - rv * ex1x2) / ess
        for j in range(0, window):
            beta.append((rv * alpha) / (1 - alpha))
            ##    print beta
        i = i - 1

    venous_ref = []
    for i in range(0, length - nT):
        venous_ref.append(x1[nT + i] - beta[i] * x2[nT + i])

    xf1, ef1, wf1 = adf.nlms(venous_ref, x2[nT:], 2 * order, 1)

    data2 = data2 + list(xf1)

    length = len(data2)
    wave = thinkdsp.Wave(ys=data2, framerate=Fs)
    spectrum = wave.make_spectrum()
    spectrum_heart = wave.make_spectrum()
    spectrum_resp = wave.make_spectrum()

    fft_mag = list(np.absolute(spectrum.hs))
    fft_length = len(fft_mag)

    spectrum_heart.high_pass(cutoff=0.7, factor=0.001)
    spectrum_heart.low_pass(cutoff=4, factor=0.001)
    fft_heart = list(np.absolute(spectrum_heart.hs))
    spectrum_resp.high_pass(cutoff=0.15, factor=0)
    spectrum_resp.low_pass(cutoff=0.4, factor=0)
    fft_resp = list(np.absolute(spectrum_resp.hs))

    max_fft_heart = max(fft_heart)
    heart_sample = fft_heart.index(max_fft_heart)
    fund_freq = heart_sample * Fs / length * 60
    nT = int(fund_freq / 60 * Fs)
    max_fft_resp = max(fft_resp)
    resp_sample = fft_resp.index(max_fft_resp)
    rr = resp_sample * Fs / length * 60
    print "Heart rate       [normal 60-100]                       : ", fund_freq, 'BPM'
    print "Respiration Rate [normal 10-20]                        : ", rr, "RPM"
    return fund_freq,rr


##...................................................................##        

def hemoglobin(red_max, ir_max):
    try:
        y = (red_max) / 65
        z = (ir_max) / 65
        OD1 = math.log(y)
        OD2 = math.log(z)
        hbo2 = (((3226.56 * OD2) - (693.44 * OD1)) / 3695420) * 6600
        hhb = (((1214 * OD1) - (319.6 * OD2)) / 3695420) * 6600
        hb = abs(hbo2 + hhb)
        print 'Hemoglobin [ normal male 13-18 female 12-15]           : ', hb, 'gm/dL'
        return hb
    except ZeroDivisionError:
        next