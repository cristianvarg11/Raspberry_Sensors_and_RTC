#----------- Importacion de modulos ---------------#
import smbus
from math import floor
from datetime import datetime
from calendar import weekday
#------------- Definiciones para hardware ---------#
Canal = 1
RTCdir = 0x68
#------------ Dics --------------------------------#
RTCreg = {'segundos': 0x00, 'minutos': 0x01, 'hora': 0x02, 'dia': 0x03, 'fecha': 0x04, 'mes': 0x05, 'year': 0x06}
#__________________________________________________#
RTCvalor = {'segundos': float("nan"), 'minutos': float("nan"), 'hora': float("nan"), 'dia': float("nan"), 'fecha': float("nan"),
            'mes': float("nan"), 'year': float("nan")}
#__________________________________________________#
dias = {1:'domingo', 2:'lunes', 3:'martes', 4:'miercoles', 5:'jueves', 6:'viernes', 7:'sabado'}
#__________________________________________________#
meses = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio', 7:'julio', 8:'agosto',
         9:'septiembre', 16:'octubre', 17:'noviembre', 18:'diciembre'}
#--------------------------------------------------#
#<<<<<<<<<<<<<<<<< Class >>>>>>>>>>>>>>>>>>>>>>>>>>#
class DS3231:
    #________write _____________#
    @staticmethod
    def write(fecha, mes, anio, hora, minuto, segundo, formato, dia):
        if formato == 'PM':
            binformato = 0b01100000
        else:
            binformato = 0b01000000
        RTCvalor = {'segundos': segundo, 'minutos':minuto, 'hora': hora, 'dia': dia, 'fecha': fecha, 'mes': mes, 'year': anio}
        for llave in RTCvalor.keys():
            if RTCvalor[llave] > 9:
                decena = floor(RTCvalor[llave]/10)
                unidad = RTCvalor[llave] % 10
                RTCvalor[llave] = (decena << 4) | unidad
        RTCvalor['hora'] = RTCvalor['hora'] | binformato
        bus = smbus.SMBus(Canal)
        for llave in RTCreg.keys():
            bus.write_byte_data(RTCdir, RTCreg[llave], RTCvalor[llave])
    #_________ Read _____________#
    @staticmethod
    def Read():
        bus = smbus.SMBus(Canal)
        for llave in RTCreg.keys():
            RTCvalor[llave] = bus.read_byte_data(RTCdir, RTCreg[llave])
        auxiliar = RTCvalor['hora'] & 0b00100000
        RTCvalor['hora'] = RTCvalor['hora'] & 0b00011111
        if auxiliar == 0b00100000:
            formatohora = 'PM'
        else:
            formatohora = 'AM'
        Lectura ='''=============== Fecha y Hora ===============
        \r{}, {:02x} de {} del 20{:02x}
        \r{:02x}:{:02x}:{:02x} {}
        \r============================================\n'''.format(
                    dias[RTCvalor['dia']], RTCvalor['fecha'], meses[RTCvalor['mes']],
                    RTCvalor['year'], RTCvalor['hora'], RTCvalor['minutos'], RTCvalor['segundos'], formatohora)
        return Lectura
#--------------------------------------------------#
class Local_and_RTC(DS3231):  # Sincronizar datos si entre el RTC el localtime existen mas de 2 seg de diferencia
    #________ Capture ___________#
    def __init__(self):
        now = datetime.now()  # fecha y hora del sistema
        #------ data ------#
        self.data = {'segundos': now.second, 'minutos': now.minute, 'hora': now.hour, 'fecha': now.day, 'mes': now.month, 'year': now.year}
        self.day_week = weekday(self.data['year'], self.data['mes'], self.data['fecha'])
        #------------------#
        # to write in DS3231
        if self.data['mes'] > 9:
            self.data['mes'] = (self.data['mes'] - 4) + 10
        if self.data['hora'] >= 12:
            self.formato = 'PM'
            self.data['hora'] = self.data['hora'] - 12
            if self.data['hora'] == 0:
                self.data['hora'] = 12
        else:
            self.formato = 'AM'
    #________ Sincroni __________#
    def Sincroni(self):
        Actual = self.data['segundos'] - RTCvalor['segundos']
        if Actual >= 2:
            self.write(self.data['year'], self.data['mes'], self.data['year'], self.data['hora'], self.data['hora'], self.data['segundos'], self.formato, dias[self.day_week + 2])
#<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>#
if __name__ == '__main__':
    #------- Fijar fecha y hora ------------#
    # DS3231.write(14, 7, 20, 4, 2, 00, 'PM', 3)
    #---------------------------------------#
    ahora = DS3231.Read()
    print(ahora)
#<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>#
  