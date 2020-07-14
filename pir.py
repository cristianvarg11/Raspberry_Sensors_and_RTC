#------------- Importacion de modulos ---------------#
from rtc import*
from dht import*
#------------ Definiciones de hardware --------------#
sensorPIR = 40
alarma = 36
GPIO.setup(sensorPIR, GPIO.IN)
GPIO.setup(alarma, GPIO.OUT)
#----------------------------------------------------#
#<<<<<<<<<<<<<<<< Class >>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
class Sensor_PIR(DS3231):
    def __init__(self, habitacion):
        self.habitacion = habitacion
        self.Lectura = self.Read()
    #__________________________________________#
    def __str__(self):
        return  f"<<<<<<<<<<<<<<<<<<<< Sensor PIR #{self.habitacion}>>>>>>>>>>>>>>>>>>>>>>\n"\
                f"{self.Lectura}\n"\
                f"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>#
