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
nombre=nombre+input('Inserta nombre: ') #define el nombre del log
nombre=nombre+'.csv'

cabecera=0 #flag para saber si acabó la cabecera
x=0 #variable para las lecturas
s="11111111\r\n" #señal de inicio de cabecera
s=s.encode("utf-8")     #codificamos en bits para la comparación    
                       
input('Wait for Arduino LED and Click Enter')#espera a que el usuario clique enter
ser1.write(bytes('00000001','utf-8')) #envía la señal de arranque alarduino vía puerto serie 
print("Señal de arranque enviada")

file1 = open(nombre, 'w') #abre el archivo en modo write (si existe sobreescribe)
date=datetime.now() #lee la fecha
dia= date.strftime('%A, %d. %B %Y')#fecha -> dia string
hora = date.strftime('%H:%M:%S') #fecha -> hora string
file1.write("Día;")        #escribe el día
file1.write(dia) 
file1.close()  

file1 = open(nombre, 'a') #abre el archivo en modo append

file1.write(";Hora de Inicio;")# escribe la hora
file1.write(hora)
file1.write('\n')
file1.close() 
print("Fecha:   ",dia) #Printea Fecha y hora de inicio
print("Hora de Inicio:",hora)

while (cabecera==0): #mientras no se active el flag de cabecera
        x=ser1.readline() #lee el serial y guardalo en x
        if  x==s : #si x es la señal de final de cabecera
                cabecera=1 #activa el flag
                x=ser1.readline() #lee el serial y guardalo en x
                x=x.decode('utf-8') #conviertelo a string 
                print("Se ha finalizado el setup, comienza el log")
                file1 = open(nombre, 'a') #abre el archivo en modo append
                file1.write(x)   
                file1.close
        else: #de lo contrario, printea la cabecera
                
                x=x.decode('utf-8') #conviertelo a string 
                
                print(x)
                      

while (cabecera==1): #mientras no pulses q
        date=datetime.now() #lee la fecha
        dia= date.strftime('%A, %d. %B %Y')#fecha -> dia string
        hora = date.strftime('%H:%M:%S') #fecha -> hora string

        if(ser1.in_waiting>0 and os.path.exists(nombre)): #si el archivo existe y acabó la cabecera
                         file1 = open(nombre, 'a') #abre el archivo en modo append
                         x=ser1.readline() #lee el serial y guardalo en x
                         file1.write(hora) #escribe la hora en la primera linea
                         file1.write(';')             
                         x=x.decode('utf-8') #convierte x a string
                         file1.write(x)  #escribe x (datos recibidos de arduino)
                         file1.write('\n')   #siguiente línea
                         file1.close()
                        
                               
                                        
                
               
      
        