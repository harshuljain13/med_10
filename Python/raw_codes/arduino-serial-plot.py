import serial
from array import array
import numpy as np
from matplotlib import pyplot as plt

ser = serial.Serial('COM4', 9600)
plt.ion()
length=60
axes1=plt.axes()
plt.ylim([-3,3])
plt.yticks(np.arange(0,1050,40))
plt.ylabel('ADC values')

plt.grid()
axdata = [0] * length

line1, = plt.plot(axdata,linewidth=2)

while True:
    sensor=ser.readline()
    sensorvalue=int(sensor)
    axdata.append(sensorvalue)
    del axdata[0]
    line1.set_xdata(np.arange(len(axdata)))
    line1.set_ydata(axdata)
    plt.draw()
    

    
