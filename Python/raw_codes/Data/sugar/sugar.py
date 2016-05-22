import time
import math
import serial

time.sleep(1)
red_max=0
ir_max=0
red_min=850
ir_min=850
count=0

ser=open('harshulmom-beforemeal_203.txt','r',1)

##ser = serial.Serial('COM45', 115200)

while True:
    try:
        sensor=ser.readline()
        if sensor is '':
            break
        count+=1
        a= sensor.split(' ')
        
        analog_red=int(a[0])
        analog_ir=int(a[1])
        
        if count ==100:
            count=0
            red_ac= float(red_max-red_min)
            ir_ac= float(ir_max-ir_min)
            ana_ir=float(ir_max)
            absorption=float((ana_ir*ana_ir))/1023
            print absorption
            red_max=0
            ir_max=0
            red_min=850
            ir_min=850
            
        
        else:
            if analog_red> red_max :
                red_max=analog_red
            elif analog_red< red_min :
                red_min=analog_red
                
            if analog_ir> ir_max:
                ir_max=analog_ir
            elif analog_ir< ir_min :
                ir_min=analog_ir
        
        
    except ZeroDivisionError:
        next

    
        
    
