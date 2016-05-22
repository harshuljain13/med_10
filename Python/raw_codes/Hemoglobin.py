import time
import math

time.sleep(1) # delays for 1 seconds
red_max=0
ir_max=0
red_min=850
ir_min=850
count=0

valuesfile=open('Data/shobhit_spo2_16ms_motion1.txt','r',1)

##for i in range(0,50):
##    sensor=ser.readline()
avgred=0
avgir=0
for sensor in valuesfile:
#while True:
    try:
        #sensor=ser.readline()
        #if sensor is '':
        #    break
        count+=1
        a= sensor.split(' ')
        analog_red=int(a[0])
        analog_ir=int(a[1])
        avgred=avgred+analog_red
        avgir=avgir+analog_ir
        

        if count ==100:
            count=0
            red_ac= float(red_max-red_min)
            ir_ac= float(ir_max-ir_min)
            y=red_max/100
            z=ir_max/100
            OD1=math.log(y)
            OD2=math.log(z)
            hbo2=(((3226.56*OD2)-(693.44*OD1))/3695420)*6600
            hhb=(((1214*OD1)-(319.6*OD2))/3695420)*6600
            hb=abs(hbo2+hhb)
            print 'Hemoglobin : ',hb
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

##        time.sleep(0.1)

    
        
    
