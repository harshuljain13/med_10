import numpy as np
from array import array
from matplotlib import pyplot as plt
from pylab import *
import math
import cmath
N1=3111
L=10
j=1
T=0.001
N=100

''''
take data from stuff!!!
x111
y111
'''

x111=np.empty(3111)
y111=np.empty(3111)
y112=np.empty(3111)


for cntr in range(1,3111):
    x111[cntr-1]=cntr
    y111[cntr-1]=1*math.sin(314.1416*cntr*T)+3*math.sin(2*314.1416*cntr*T)
    y112[cntr-1]=0.9*math.sin(314.1416*cntr*T)+2.8*math.sin(2*314.1416*cntr*T)


#y111=np.random.randn(3111)

y=np.empty(100)
x=np.empty(100)
yn=np.empty(100)
for cntr in range(1,100):
    x[cntr-1]=cntr

N2= int(math.floor(N1/100))
vk=np.empty([10,N2])
freqk=np.empty([10,N2])
alphak=np.empty([10,N2])
phasek=np.empty([10,N2])
avgk=np.empty([2,N2])
spO2=np.empty(N2)
parameters=np.empty([13,N2])

SimulatedOutput=np.empty(N)




num=1
for num in range(0,N2-1):
    for cntr in range(0,100):
        x[cntr]=num*100+cntr-1
        y[cntr]=y111[num*100+cntr+1]
        yn[cntr]=y112[num*100+cntr+1]
    N=100
    suom=0
    sumi=0
    acsum=0
    acsum1=0
    #plt.plot(x,y)
    #plt.hold(True)
    for cntr in range(1,100):
        suom=suom+y[cntr-1]
        acsum=acsum+y[cntr-1]*y[cntr-1]
        sumi=sumi+yn[cntr-1]
        acsum1=acsum1+yn[cntr-1]*yn[cntr-1]
    avg=suom/N
    avg1=sumi/N
    ac=math.sqrt(acsum/N)
    ac1=math.sqrt(acsum1/N)
    for cntr in range(1,100):
        y[cntr-1]=y[cntr-1]-avg
        yn[cntr-1]=yn[cntr-1]-avg1
    #plt.plot(x,y)
    #plt.hold(True)
    #formation of d
    d=np.empty(N-L)
    j=1
    for cntr in range(L,N):
        d[j-1]=y[cntr]
        j=j+1
    #formation of D
    D=np.empty([N-L,L])
    r=1
    c=1
    for cntr in range(1,N-L+1):
        for cntr1 in range(1,L+1):
            D[r-1,c-1]=y[L-cntr1+cntr-1]
            c=c+1
        c=1
        r=r+1
    
    inversa=np.linalg.pinv(D)
    a=np.empty(L)
    a=np.dot(inversa,d)
    #obtaining z roots
    z=np.empty(11)
    for cntr in range(0,11):
        if cntr==0:
            z[cntr]=1
        else:
            z[cntr]=-a[cntr-1]
    rots=np.roots(z)

    #formation of y=uc and y=y1
    y1=np.empty(L)
    for cntr in range(0,L):
        y1[cntr]=y[L+cntr-1]

    
    u=np.empty([L,L],complex)
    c1=np.empty(L)

    r=1
    c=1
    for cntr in range(1,L+1):
        for cntr1 in range(1,L+1):
            u[r-1,c-1]=u[r-1,c-1]+0j
            u[r-1,c-1]= pow(rots[cntr1-1],r-1)
            c=c+1
        c=1
        r=r+1
       
    c1=np.dot(np.linalg.pinv(u),y1)
#amplitude
    
    val=np.empty(L)
    for cntr in range(0,L-1):
        val[cntr]=abs(c1[cntr]*2)
#frequency
    f=np.empty(L)
    for cntr in range(0,L-1):
        re=rots[cntr].real
        im=rots[cntr].imag
        kk=2*3.1416*T
        if re!=0:
            f[cntr]=math.atan(im/re)/kk

    phi=np.empty(L)
    for cntr in range(0,L):
       # print c1[cntr].real , c1[cntr].imag
        if c1[cntr].real==0:
           phi[cntr]=cmath.pi/2
        else:
            real=c1[cntr].imag
            imaginary=c1[cntr].real
            if real!=0:
                phi[cntr]=math.atan(imaginary/real)
            else:
                phi[cntr]=0
                val[cntr]=0
                f[cntr]=0
    for cntr in range(0,L-1):
        if f[cntr]<0.2 or f[cntr]<-0.0:
            val[cntr]=0
            phi[cntr]=0
            f[cntr]=0
    hasChanged=True
    itemCount=10
    while(hasChanged):
        hasChanged=False
        itemCount=itemCount-1
        for index in range(1,itemCount):
            if f[index]>f[index+1]:
                tmp=val[index]
                val[index]=val[index+1]
                val[index+1]=tmp
                tmp=f[index]
                f[index]=f[index+1]
                f[index+1]=tmp
                tmp=phi[index]
                phi[index]=phi[index+1]
                phi[index+1]=tmp
#    for cntr in range(1,N):
        #SimulatedOutput[cntr]=SimulatedOutput[cntr]
 #       for cntr1 in range(1,L):
  #          SimulatedOutput[cntr-1]=SimulatedOutput[cntr-1]+val[cntr1]*math.sin(phi[cntr1-1]+2*3.1416*f[cntr1-1]*cntr*T)
   #               
    #plt.plot(x*T,y)
    #plot.hold=True
    #plt.plot(x*T,SimulatedOutput)
    #plot.hold=True

#the figures
    for cntr in range(0,9):
        vk[cntr,num]=val[cntr] 
        freqk[cntr,num]=f[cntr]
        phasek[cntr,num]=phi[cntr]
        print val[cntr],'   ',f[cntr],'   ',phi[cntr],'   ',avg,'   '
    print '\n'
    avgk[0,num]=avg
    avgk[1,num]=avg1
    spO2[num-1]=(ac/avg)/(ac1/avg1)
    for pas in range(1,5):
        parameters[pas-1,num]=freqk[4+pas,num]
    for pas in range(6,10):
        parameters[pas-1,num]=vk[pas-1,num]
    parameters[10,num]=avg
    parameters[11,num]=avg1
    parameters[12,num]=spO2[num]
    
          
    
        
#plt.show()

