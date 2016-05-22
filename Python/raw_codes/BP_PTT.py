import time

time.sleep(1) # delays for 1 seconds
##red_max=0
##ir_max=0

red_prev=0
red_curr=0
ir_prev=0
ir_curr=0

ir=0
red=0

count=0
count1=0
total=0

red_slope=-1
ir_slope=-1
red_sample=0
ir_sample=0

valuesfile=open('Data/bp_ptt_abhi-forearm_filtered2.txt','r',1)

for value in valuesfile:
    if value is '': break
    count+=1
    a= value.split(' ')
    if a[0] is '' or a[1] is '':break
    red_curr=int(a[0])
    ir_curr=int(a[1])

    if red_slope == -1:
        if red_curr > red_prev: red_slope=1

    elif red_slope==1:
        if red_curr < red_prev:
            red_slope=-1
            red_sample=count
            red=1
##            print "Red:", red_sample
            
    if ir_slope == -1:
        if ir_curr > ir_prev: ir_slope=1

    elif ir_slope ==1:
        if ir_curr < ir_prev:
            ir_slope=-1
            ir_sample=count
            ir=1
##            print "IR:", ir_sample

    if ir and red:
        total= total + (ir_sample - red_sample)
        count1+=1
        ptt=total/count1
        print ptt
        ir=0
        red=0
 
    red_prev=red_curr
    ir_prev=ir_curr

ptt=abs(float(ptt)*2/1000)
print "PTT:", ptt, "sec"
d=0.45  #distance between the two points in meters
constant_A=740*(d**2)
constant_B=14490
height_diff=0.05   #height difference between the two points in meters
BP=constant_A/ptt**2 + constant_B*height_diff
BP=BP*7.5006/1000   ##convert from Pa(kg/ms2) to mmHg
print "BP:", BP, "mmHg"


    
    
    
