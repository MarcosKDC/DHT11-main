from datetime import datetime
from time import sleep, strftime, time
import keyboard
import serial
import os.path

ser1 = serial.Serial( #DEFINICIÓN DEL PUERTO SERIe A UTILIZAR
        port='COM3',        # Serial Port to read the data from
        baudrate = 9600,        #Rate at which the information is shared to the communication channel
        parity=serial.PARITY_NONE, #Applying Parity Checking (none in this case)
        stopbits=serial.STOPBITS_ONE,       # Pattern of Bits to be read
        bytesize=serial.EIGHTBITS,        # Total number of bits to be read
        timeout=1        # Number of serial commands to accept before timing out
)

nombre='logTemperatura'
nombre=nombre+input('inserta nombre') #define el nombre del log
nombre=nombre+'.csv'

cabecera=0
x=0
while not(keyboard.is_pressed("q")): #mientras no pulses q

        date=datetime.now() #lee la fecha
        dia= date.strftime("%A, %d. %B %Y")#fecha -> dia string
        hora = date.strftime("%H:%M:%S") #fecha -> hora string
        print(hora) #printea la hora

        if(os.path.exists(nombre) and cabecera==2): #si el archivo existe y acabó la cabecera
                file1 = open(nombre, 'a') #abre el archivo en modo append

                file1.write(hora)
                file1.write('\n')             
           
                x=ser1.readline() #lee el serial y guardalo en x
                x=x.decode("utf-8") #conviertelo a string
                file1.write(x)  
                x=ser1.readline() #lee el serial y guardalo en x
                x=x.decode("utf-8") #conviertelo a string
                file1.write(x)  

                file1.close() 
                
        else: # si el archivo no existe espera a que cliques enter, manda la señal de arranque al setup del arduino  y crea la cabecera,
                file1 = open(nombre, 'w') #abre el archivo
        
                file1.write(dia)
                file1.write('\n')
                file1.close()  

                file1 = open(nombre, 'a') #abre el archivo en modo append
                file1.write(hora)# escribe la hora
                file1.write('\n')
                file1.close() 
 
                input("Reset Arduino and Click Enter")

                ser1.write(bytes('00000001','utf-8')) #envía la señal de encendido al puerto serie
                while cabecera==0:
                        x_ant=x
                        x=ser1.readline() #lee el serial y guardalo en x
                        x=x.decode("utf-8") #conviertelo a string 
                        if  x_ant== x: #si llega inicio cabecera
                                cabecera==1
                                x=ser1.readline() #lee el serial y guardalo en x
                                x=x.decode("utf-8") #conviertelo a string 
                                print(x)
                                while x_ant !=x:
                                        file1 = open(nombre, 'a') #abre el archivo en modo append
                                        file1.write(x)   
                                        x=ser1.readline() #lee el serial y guardalo en x
                                        x=x.decode("utf-8") #conviertelo a string 
                                        file1.close
                                       
                
               
      
        