import serial
import numpy as np
from matplotlib import pyplot as plt
from array import array

sensordata = array("f")

ser = serial.Serial('COM18', 9600)
plt.ion()
length=100
axes1=plt.axes()
plt.ylim([-3,3])
plt.yticks(np.arange(0,1050,40))
plt.ylabel('ADC values')
plt.grid()
axdata = [0] * length

line1, = plt.plot(axdata)

while True:
    for j in range(0,100):
        sensor=ser.readline()
        sensorvalue=1024-float(sensor)
        sensordata.append(sensorvalue)
        #print sensordata[j]
        axdata.append(sensordata[j])
        del axdata[0]
        line1.set_xdata(np.arange(len(axdata)))
        line1.set_ydata(axdata)
        plt.draw()
    

    
