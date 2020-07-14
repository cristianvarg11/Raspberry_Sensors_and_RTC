#------------ Importacion de modulos ----------------#
import RPi.GPIO as GPIO
from time import sleep
from colorama import Fore,init ; init()
#----- Modulos locales ------#
from rtc import *
#------------ Definiciones --------------------------#
pinDHT = 19
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinDHT, GPIO.OUT)
Retardo = lambda x: sleep(x)
msRetardo = lambda x: sleep(x/1000)
dhtOK = 0
#----------- Errores de comunicacion ----------------#
class Errores (Exception):
    pass
class ErrorTimeOut(Errores):
    pass
class ErrorChecksum(Errores):
    pass
#<<<<<<<<<<<<<<<< Class >>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
class DHT11:
    #__________________________________________#
    @staticmethod
    def Verificar(espera, valor, tiempo):
        for i in range (espera):
            if GPIO.input(pinDHT) == valor and tiempo == False:
                return dhtOK
            if GPIO.input(pinDHT) == valor and tiempo == True:
                return i
        raise ErrorTimeOut(Fore.RED + 'Se excede el contador establecido')
    #__________________________________________#
    @staticmethod
    def datos():
        resultado = 0
        for i in range (8):
            ValorA = DHT11.Verificar(100, True, True)
            ValorB = DHT11.Verificar(100, False, True)
            resultado = resultado | (ValorA < ValorB) << (7 - i)
        return resultado
    #__________________________________________#
    @staticmethod
    def leer():
        #--- Inicio de comunicacion ---#
        GPIO.setup(pinDHT, GPIO.OUT)
        GPIO.output(pinDHT, True)
        GPIO.output(pinDHT, False)
        msRetardo(20)
        GPIO.output(pinDHT, True)
        GPIO.setup(pinDHT, GPIO.IN)
        #--- esperar hasta 40us por una resp ---#
        DHT11.Verificar(100, False, False)
        #--- Cuando se da False, esperar hasta 90us por True ---#
        DHT11.Verificar(100, True, False)
        #--- Cuando se da el True, esperar por el inicio de datos ---#
        DHT11.Verificar(100, False, False)
        humedad = DHT11.datos()
        humedad_dec = DHT11.datos()
        temp_int = DHT11.datos()
        temp_dec = DHT11.datos()
        Checksum = DHT11.datos()
        VerificarCheck = humedad + humedad_dec + temp_int + temp_dec
        if VerificarCheck != Checksum:
            raise ErrorChecksum(Fore.RED + 'No coincide el CheckSum')
        GPIO.setup(pinDHT, GPIO.OUT)
        GPIO.output(pinDHT, True)
        sensorDHT = {'Humd': humedad, 'HumdDec': humedad_dec, 'TempA': temp_int, 'TempB': temp_dec, 'CheckSum': Checksum}
        return sensorDHT
#--------------------------------------------------#
class dht(DHT11):
    def __init__(self):
        try:
            self.medicion = self.leer()
        except ErrorTimeOut:
            self.medicion = {'Humd': 'E1', 'TempA': 'E1', 'TempB': 'E1'}
        except ErrorChecksum:
            self.medicion = {'Humd': 'C2', 'TempA': 'C2', 'TempB': 'C2'}
    #__________________________________________#
    def __str__(self):
        return  f"========= Medicion de Temperatura y Humedad ==========\n"\
                f"Humedad: {self.medicion['Humd']}%\n"\
                f"Temperatura: {self.medicion['TempA']},{self.medicion['TempB']}"\
                f"* Celsius\n"\
                f"======================================================\n"
#<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>#
