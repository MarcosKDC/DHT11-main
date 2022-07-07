from datetime import datetime
from time import sleep, strftime, time
from tokenize import cookie_re
import keyboard
import serial
import os.path
import matplotlib.pyplot as plt
import numpy as np
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
s= "11111111\r\n" #señal de inicio de cabecera
s=s.encode("utf-8")     #codificamos en bits para la comparación
on=True
data=[]
graphx=[]
graphtemp=[]
graphhum=[]
plt.ion()
while (True): #mientras no pulses q
        ser1.flush()
        if(keyboard.is_pressed('up')):
                 on=True
        if(on):
                ser1.write(bytes(chr(1),'utf-8'))
                if(keyboard.is_pressed('down') and keyboard.is_pressed('left') and keyboard.is_pressed('right')):
                        on=False
                date=datetime.now() #lee la fecha
                dia= date.strftime('%A, %d. %B %Y')#fecha -> dia string
                reloj = date.strftime('%H:%M:%S') #fecha -> reloj string
                if(cabecera==1): #si el archivo existe y acabó la cabecera
                        while(ser1.in_waiting>0):
                                file1 = open(nombre, 'a') #abre el archivo en modo append
                                x=ser1.readline() #lee el serial y guardalo en x
                                ser1.flushInput()
                                x=x.strip()
                                file1.write(reloj) #escribe la reloj en la primera linea
                                file1.write('; ')             
                                x=x.decode('utf-8') #convierte x a string
                                file1.write(x)  #escribe x (datos recibidos de arduino)
                                file1.write('\n')   #siguiente línea
                                file1.close() 
                                data=x.split(';')
                                [hora,minuto,segundo]= reloj.split(':')

                                tiempo=round(float(hora)+float(minuto)/60+float(segundo)/3600,3)
                                try:
                                        graphtemp.append(float(data[0]))
                                        graphhum.append(float(data[1]))
                                        graphx.append(tiempo)
                                except ValueError:
                                        continue
                                plt.plot(np.array(graphx),np.array(graphtemp),'k-')
                                ##plt.plot(np.array(graphx),np.array(graphhum),'g-')
                                plt.show()
                                plt.pause(0.1)
                else: # si no acabó la cabecera 
                        input('Wait for Arduino LED and Click Enter')#espera a que el usuario clique enter
                        ser1.write(b'1') #envía la señal de arranque al arduino vía puerto serie
                        print("Señal de arranque enviada")
                        if(not(os.path.exists(nombre))):#si el archivo no existe espera a que cliques enter,
                                
                                file1 = open(nombre, 'w') #abre el archivo en modo write (si existe sobreescribe)
                                
                                file1.write("Dia;       ")        #escribe el día
                                file1.write(dia) 
                                file1.close()  
                        
                                file1 = open(nombre, 'a') #abre el archivo en modo append
                                file1.write(";  Hora de Inicio;    ")# escribe la reloj
                                file1.write(reloj)
                                file1.write('\n')
                                file1.close()         
                        print("Fecha:   ",dia) #Printea Fecha y reloj de inicio
                        print("Hora de Inicio:  ",reloj)
                        while cabecera==0: #mientras no se active el flag de cabecera
                                x=ser1.readline() #lee el serial y guardalo en x
                                if  x==s : #si x es la señal de final de cabecera
                                        cabecera=1 #activa el flag
                                        x=ser1.readline() #lee el serial y guardalo en x
                                        x=x.strip()
                                        x=x.decode('utf-8') #conviertelo a string 
                                        print("Se ha finalizado el setup, comienza el log")
                                        file1 = open(nombre, 'a') #abre el archivo en modo append
                                        file1.write(x)   #printea la cabecera
                                        file1.write('\n') 
                                        file1.close
                                else: #de lo contrario, printea la cabecera
                                        x=x.decode('utf-8') #conviertelo a string
                                        print(x)
        else: 
                ser1.write(bytes(chr(0),'utf-8'))
                if(ser1.in_waiting>0):
                        x=ser1.readline() #lee el serial y guardalo en x
                        x=x.strip()
                        x=x.decode('utf-8') #conviertelo a string 
                        print(reloj) #escribe la reloj en la primera linea   
                        print(x)
                        data=x.split(';')
                        [hora,minuto,segundo]= reloj.split(':')
                plt.show()
                plt.pause(1)
                      
                        
                               
                                        
                
               
      
        