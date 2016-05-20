import serial
import thinkdsp
from matplotlib import pyplot as plt
import numpy as np
from multiprocessing import Process


Fs=4.167#sampling frequency in Hz, e.g. sampling interval=80 ms Fs=12.5Hz
SpO2=99

def estimate(data):
    length=len(data)
    wave=thinkdsp.Wave(ys=data,framerate=Fs)
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
    else:
        print "Respiration Rate:", rr, "RPM"
    
    return


if __name__ == '__main__':
    ser = serial.Serial('COM4', 9600)
##    valuesfile=open('Data/abhishek_new_sensor_short_quick_resp.txt','r',1)
    data=[]
    time=float (0)
    count=0

    while True:
        time=count/Fs
##        print "time:" ,time
        if time<7:
            sensor=ser.readline()
            if sensor is '':
                break
            count+=1
            data.append(int(sensor))
        else:
            count=0
            p = Process(target=estimate, args=(data,))
##            estimate(data)
            del data
            data=[]
            p.start()
        
