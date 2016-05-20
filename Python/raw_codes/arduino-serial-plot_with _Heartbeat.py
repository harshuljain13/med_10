import serial
from array import array
import numpy as np
from matplotlib import pyplot as plt

ser = serial.Serial('COM18', 115200)

plt.ion()
length=192
axes1=plt.axes()
plt.ylim([-3,3])
plt.yticks(np.arange(0,1050,40))
plt.ylabel('ADC values')
plt.grid()
axdata = [0] * length

line1, = plt.plot(axdata)

count=0
lastBeatTime=0
Pulse=0
QS=0
P=512
T=512
thresh=525
amp=100
firstBeat=1
secondBeat=0
IBI=600
BPM=0
rate=[]

#valuesfile=open('ppg1.txt','r',1)
while True:
    sensor=1023-int(ser.readline())
    #sensor=1023-int(valuesfile.readline())
    axdata.append(sensor)
    del axdata[0]
    line1.set_xdata(np.arange(len(axdata)))
    line1.set_ydata(axdata)
    plt.draw()
    
    count+=192
    N=count-lastBeatTime
    
    if sensor < thresh and N> (IBI/5)*3:
        if sensor<T:
            T=sensor
    
    if sensor > thresh and sensor > P:
        P=sensor
    
    if N>250:
        if sensor>thresh and Pulse==0 and N> (IBI/5)*3:
            Pulse=1
            IBI=count-lastBeatTime
            lastBeatTime=count

            if secondBeat:
                secondBeat=0;
                for i in range(0,10):
                    rate.append(IBI)

            if firstBeat:
                firstBeat=0
                secondBeat=1
                continue
            
            runningTotal=0
            for i in range(0,9):
                rate[i]=rate[i+1]
                runningTotal+=rate[i]

            rate[9]=IBI
            runningTotal+=rate[9]
            runningTotal/=10
            BPM=60000/runningTotal
            QS=1


    if sensor<thresh and Pulse==1:
        Pulse=0
        amp=P-T
        thresh=amp/2+T
        P=thresh
        T=thresh

    if N>2500:
        thresh=512
        P=512
        T=512
        lastBeatTime=count
        firstBeat=1
        secondBeat=0

    if QS==1:
        print "Heart Rate:",BPM,"bpm"
