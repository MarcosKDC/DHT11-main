from datetime import datetime
from time import sleep, time
import keyboard
import serial
import os.path
nombre='logTemperatura.txt'
n=0
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
while not(keyboard.is_pressed("q")):
        date=datetime.now()
        dia= date.strftime("%A, %d. %B %Y")
        hora2 = date.strftime("%H:%M:%S")
        print(hora2)
       

        if(os.path.exists(nombre)):
                file1 = open(nombre, 'a')
                file1.write(hora2)
                file1.write('\n')
                for i in range(n):
                        x=ser1.readline()
                        x=x.decode("utf-8")
                        file1.write(x)   
                file1.close()  
                n=2 
        else:
                n=5
                file1 = open(nombre, 'w')
                file1.write(dia)
                file1.write('\n')
                file1.close()  
                input()
 
      
        