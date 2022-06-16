from datetime import datetime
from time import sleep, time
import keyboard
import serial

date=datetime.now
ser1 = serial.Serial(
        # Serial Port to read the data from
        port='COM3',
 
        #Rate at which the information is shared to the communication channel
        baudrate = 9600,
   
        #Applying Parity Checking (none in this case)
        parity=serial.PARITY_NONE,
 
       # Pattern of Bits to be read
        stopbits=serial.STOPBITS_ONE,
     
        # Total number of bits to be read
        bytesize=serial.EIGHTBITS,
 
        # Number of serial commands to accept before timing out
        timeout=1
)
ser2 = serial.Serial(
        # Serial Port to read the data from
        port='COM1',
 
        #Rate at which the information is shared to the communication channel
        baudrate = 9600,
   
        #Applying Parity Checking (none in this case)
        parity=serial.PARITY_NONE,
 
       # Pattern of Bits to be read
        stopbits=serial.STOPBITS_ONE,
     
        # Total number of bits to be read
        bytesize=serial.EIGHTBITS,
 
        # Number of serial commands to accept before timing out
        timeout=1
)
while 1:
        x=ser1.readline()
        date=datetime.now()
        hora2 = date.strftime("%H:%M:%S")
        print(hora2)
        print (x)
        if (keyboard.is_pressed('q')):
                ser2.write(bytes("La temperatura alcanzada, a las ",'utf-8'))
                ser2.write(bytes(hora2,'utf-8'))
                ser2.write(bytes(" es inadecuada",'utf-8'))
                ser2.write(bytes('\r\n','utf-8'))
                ser2.write (x)
                print(ser2.readline())
        