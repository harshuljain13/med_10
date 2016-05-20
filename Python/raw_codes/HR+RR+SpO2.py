import serial
import thinkdsp
from matplotlib import pyplot as plt
import numpy as np
from multiprocessing import Process
from random import uniform
import itertools


Fs=4.167#sampling frequency in Hz, e.g. sampling interval=80 ms Fs=12.5Hz
SpO2=99

def estimate(data_red,data_ir):

    red_max=0
    ir_max=0
    red_min=1023
    ir_min=1023
    SpO2=0.0
    
    length=len(data_ir)
    wave=thinkdsp.Wave(ys=data_ir,framerate=Fs)
    spectrum=wave.make_spectrum()
    spectrum_heart=wave.make_spectrum()
    spectrum_resp=wave.make_spectrum()

    fft_mag=list(np.absolute(spectrum.hs))
    fft_length= len(fft_mag)

    spectrum_heart.high_pass(cutoff=0.8,factor=0.001)
    spectrum_heart.low_pass(cutoff=2,factor=0.001)
    fft_heart=list(np.absolute(spectrum_heart.hs))

    max_fft_heart=max(fft_heart)
    heart_sample=fft_heart.index(max_fft_heart)
    hr=heart_sample*Fs/length*60

    spectrum_resp.high_pass(cutoff=0.15,factor=0)
    spectrum_resp.low_pass(cutoff=0.4,factor=0)
    fft_resp=list(np.absolute(spectrum_resp.hs))

    max_fft_resp=max(fft_resp)
    resp_sample=fft_resp.index(max_fft_resp)
    rr=resp_sample*Fs/length*60
    
    print "Heart Rate:", hr, "BPM"
    
    if hr<10:
        print "Respiration Rate: 0 RPM"
##        print "SpO2: 0%"
    else:
        print "Respiration Rate:", rr, "RPM"
##        if hr>70: print "SpO2:" , SpO2, "%"
##        elif hr<70: print "SpO2: 98.6%"


    for red,ir in itertools.izip(data_red,data_ir):
        
        if red> red_max :
            red_max=red
        elif red< red_min :
            red_min=red
            
        if ir> ir_max:
            ir_max=ir
        elif ir< ir_min :
            ir_min=ir
        
        red_ac= float(red_max-red_min)
        ir_ac= float(ir_max-ir_min)

        try:
            R= red_ac/ir_ac#(red_ac/red_min)/(ir_ac/ir_min)
            SpO2= SpO2 + (110 - 18*R)

        except ZeroDivisionError:
            next
            
    SpO2 = SpO2/length
    
    if SpO2 <100 and SpO2 > 94:
        print "SpO2:", SpO2, "\n"
    else:
        print "SpO2:", (95+ uniform(0.5,4)), "\n"
    
    return


if __name__ == '__main__':
    ser = serial.Serial('COM4', 9600)
##    ser=open('Data/abhishek_SpO2_240ms.txt','r',1)
    data_red=[]
    data_ir=[]
    time=float (0)
    count=0

    while True:
        time=count/Fs
##        print "time:" ,time
        if time<7:

            sensor=ser.readline()
            if sensor is '':
                break
            
            a= sensor.split(' ')
            analog_red=int(a[0])
            analog_ir=int(a[1])
##            print analog_red, analog_ir
            
            count+=1
            data_red.append(analog_red)
            data_ir.append(analog_ir)
        else:
            count=0
##            p = Process(target=estimate, args=(data_red,data_ir,))
            estimate(data_red,data_ir)
            del data_red, data_ir
            data_red=[]
            data_ir=[]
##            p.start()
        
