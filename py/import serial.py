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
#    ________.__       ____   ____            .__      ___.   .__                 
#   /  _____/|  |   ___\   \ /   /____ _______|__|____ \_ |__ |  |   ____   ______
#  /   \  ___|  |  /  _ \   Y   /\__  \\_  __ \  \__  \ | __ \|  | _/ __ \ /  ___/
#  \    \_\  \  |_(  <_> )     /  / __ \|  | \/  |/ __ \| \_\ \  |_\  ___/ \___ \ 
#   \______  /____/\____/ \___/  (____  /__|  |__(____  /___  /____/\___  >____  >
#          \/                         \/              \/    \/          \/     \/ 

#señales y flags
on=True#bool  de encendido
fsetup=False#bool  para saber si acabó la setup
s= "11111111\r\n"#señal de inicio de setup
s=s.encode("utf-8")#codificamos en bits para la comparación
tiempo_ant=0

#listas para el plot
graphx=[] 
graphtemp=[]
graphhum=[]

#    _____                        __   .__                         
#  _/ ____\__ __   ____    ____ _/  |_ |__|  ____    ____    ______
#  \   __\|  |  \ /    \ _/ ___\\   __\|  | /  _ \  /    \  /  ___/
#   |  |  |  |  /|   |  \\  \___ |  |  |  |(  <_> )|   |  \ \___ \ 
#   |__|  |____/ |___|  / \___  >|__|  |__| \____/ |___|  //____  >
#                     \/      \/                        \/      \/ 

def inicio():
        ser1.flushOutput()
        ser1.reset_input_buffer()
        ser1.flushInput()
        input('Wait for Arduino LED and Click Enter')#espera a que el usuario clique enter
        ser1.write(b'1') #envía la señal de arranque al arduino vía puerto serie
        print("Señal de arranque enviada")
        if(not(os.path.exists(nombre))):#si el archivo no existe espera a que cliques enter,
                        
                file1 = open(nombre, 'w') #abre el archivo en modo write (si existe sobreescribe)
                
                file1.write("Dia;       ")        #escribe el día
                file1.write(dia)  
                file1.write(";  Hora de Inicio;    ")# escribe la reloj
                file1.write(reloj)
                file1.write('\n')

                file1.write("Hora [HH:MM:SS]; Temperatura[Celsius];  Humedad[%];  OK?[I/O]") 
                file1.write('\n')

                file1.close()  

def RW(W=False):#leer, y escribir, bien al csv, bien printea
        while(ser1.in_waiting>0):#mientras haya cosas en el serial
                x=ser1.readline() #lee el serial y guardalo en x
                x=x.strip()
                x=x.decode('utf-8') #convierte x a string
                if(W):
                        if((tiempo!=tiempo_ant)):
                                print(tiempo)
                                tiempo_ant==tiempo
                                print (tiempo)
                                file1 = open(nombre, 'a') #abre el archivo en modo append
                                file1.write(reloj) #escribe la reloj en la primera linea
                                file1.write('; ')    
                                file1.write(x)  #escribe x (datos recibidos de arduino)
                                file1.write('\n')   #siguiente línea
                                file1.close() 
                                data= x.split(';')                    
                                try:#intenta dibujar
                                        graphtemp.append(float(data[0]))
                                        graphhum.append(float(data[1]))
                                        graphx.append(tiempo)
                                except ValueError:
                                        continue
                                plt.plot(np.array(graphx),np.array(graphtemp),'k-') #plotea
                                ##plt.plot(np.array(graphx),np.array(graphhum),'g-')
                else:
                        print(reloj) #escribe reloj
                        print(x)#escribe lo que diga el arduinillo
                        
        plt.show()
        plt.pause(1) 
        

#                   __                  
#    ______  ____ _/  |_  __ __ ______  
#   /  ___/_/ __ \\   __\|  |  \\____ \ 
#   \___ \ \  ___/ |  |  |  |  /|  |_> >
#  /____  > \___  >|__|  |____/ |   __/ 
#       \/      \/              |__|   

#define el nombre del log
nombre='logTemperatura'
nombre=nombre+input('Inserta nombre: ') 
nombre=nombre+'.csv'


plt.ion() #activa el plot
#  .__                           
#  |  |    ____    ____  ______  
#  |  |   /  _ \  /  _ \ \____ \ 
#  |  |__(  <_> )(  <_> )|  |_> >
#  |____/ \____/  \____/ |   __/ 
#                        |__|    
while (True): #main loop

        date=datetime.now() #lee la fecha
        dia= date.strftime('%A, %d. %B %Y')#fecha -> dia string
        reloj = date.strftime('%H:%M:%S') #fecha -> reloj string
        [hora,minuto,segundo]= reloj.split(':')
        tiempo=round(float(hora)+float(minuto)/60,3)#variable tiempo H,% (+float(segundo)/3600)
        
        if(keyboard.is_pressed('up')):
                on=True
                ser1.reset_output_buffer()
                ser1.reset_input_buffer()
                ser1.write(b'1')

        if(keyboard.is_pressed('down') and keyboard.is_pressed('left') and keyboard.is_pressed('right')):
                on=False
                ser1.reset_output_buffer()
                ser1.reset_input_buffer()
                ser1.write(b'0')      

        if(fsetup): #si acabó la setup
                RW(on)      #escribes, segun si esta encendido o no una cosa u otra
        else: # si no acabó la setup aka arduino no ha finalizado el setup
                inicio()     #arrancalo carlos
                print("Fecha:   ",dia) #Printea Fecha y reloj de inicio
                print("Hora de Inicio:  ",reloj)
                while not(fsetup): #mientras arduino no acabe el setup
                        x=ser1.readline() #lee el serial y guardalo en x
                        if  x==s : #si x es la señal de final de setup
                                fsetup=True #activa el flag
                                print("Se ha finalizado el setup, comienza el log")
                        else: #de lo contrario, printea la setup
                                x=x.decode('utf-8') #conviertelo a string
                                print(x)

                
                
                