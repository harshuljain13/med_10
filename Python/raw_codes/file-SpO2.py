import time

time.sleep(1) # delays for 1 seconds
red_max=0
ir_max=0
red_min=1023
ir_min=1023
count=0

valuesfile=open('Data/abhi_SpO2_240ms2.txt','r',1)

##for i in range(0,50):
##    sensor=ser.readline()

for sensor in valuesfile:
    try:
        count+=1
        a= sensor.split(' ')
        analog_red=int(a[0])
        analog_ir=int(a[1])
##        print analog_red, analog_ir
        
##        if count ==50:
##            count=0
##            red_max=0
##            ir_max=0
##            red_min=1023
##            ir_min=1023
        
##        else:
        if analog_red> red_max :
            red_max=analog_red
        elif analog_red< red_min :
            red_min=analog_red
            
        if analog_ir> ir_max:
            ir_max=analog_ir
        elif analog_ir< ir_min :
            ir_min=analog_ir
        
        red_ac= float(red_max-red_min)
        ir_ac= float(ir_max-ir_min)

##        print "ir_max:", ir_max
##        print "ir_min:", ir_min
##        print "red_max:", red_max
##        print "red_min:", red_min

        R= (red_ac/red_min)/(ir_ac/ir_min)
        SpO2= 110 - 20*R
        if SpO2 > 99.5:
            SpO2=99.5

        print "Spo2:", SpO2
        time.sleep(0.1)

    except ZeroDivisionError:
        next
        
    
