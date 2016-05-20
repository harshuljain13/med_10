import serial
from array import array
import numpy as np
from matplotlib import pyplot as plt

ser = serial.Serial('COM13', 9600)
plt.ion()
length=50
axes1=plt.axes()
plt.ylim([-3,3])
plt.yticks(np.arange(0,1050,40))
plt.ylabel('ADC values')

plt.grid()
axdata = [0] * length

line1, = plt.plot(axdata,linewidth=2)

while True:
##    sensor=ser.readline()
##    sensorvalue=1023-int(sensor)

    sensor=ser.readline()
    a= sensor.split(' ')
    analog_red=int(a[0])
    analog_ir=int(a[1])
    
    axdata.append(analog_red)
    del axdata[0]
    line1.set_xdata(np.arange(len(axdata)))
    line1.set_ydata(axdata)
    plt.draw()
    

    
