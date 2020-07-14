#-------------- Importacion de modulos -----------------#
from time import sleep
#---- Locales ----#
from rtc import *
from dht import *
from pir import *
#-------------------------------------------------------#
#<<<<<<<<<<<<<<<<<<<<< MAIN >>>>>>>>>>>>>>>>>>>>>>>>>>>>#
for i in range (1200):
    Local_and_RTC()  # comparar constantemente
    if GPIO.input(sensorPIR) == True:
        #========== Sensor PIR ===========#
        info = Sensor_PIR(1)
        print(info)
        GPIO.output(alarma, True)
        Retardo(3)  # encender alarma por 3 segundos
        GPIO.output(alarma, False)
        #--- Documento de texto ---#
        Registro_alarma = open('Registros_de _mov.txt', 'a+')
        Registro_alarma.write(str(info))
        Registro_alarma.close()
        #--------------------------#
        Retardo(10)
        print(f"\n\rTemporizador {i} ms\n\rSensor PIR preparado\n\r")
        #=========== DHT11 ========#
        medicion_temp_humd = dht()
        print(medicion_temp_humd)
        #--- Documento de texto ---#
        Temperatura = open('Temperatura.txt', 'a+')
        Temperatura.write(str(medicion_temp_humd))
        Temperatura.close()
    msRetardo(100)
GPIO.cleanup()
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>#
