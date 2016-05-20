import serial

ser = serial.Serial('COM4', 9600)

file1=open("Data/patients/13.txt",'ab',1);

while True:
    sensor=ser.read(50)
##    print sensor,
    file1.write(sensor)

    
