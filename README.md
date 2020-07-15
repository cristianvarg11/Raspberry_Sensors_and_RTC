# Raspberry_Sensors_and_RTC
In this project it's used the Raspberry Pi 3 model B+, the project function is: 
1. capture the system date and time to synchronize the RTC DS3231, the system must be able to detect synchronization failures between the system and the device so that if There is a difference of more than two seconds between the system time and the RTC time. automatically proceed to synchronize the RTC DS3231. 
2. Connect the motion sensor and activate it by a time window of 2 minutes, record the activation of the PIR sensor in a text document, with the detail of the date and time the detection occurred. 
3. Every time the motion sensor is activated, an alarm must be activated using a Buzzer on and off with a duration of three seconds. 
4. Connect the humidity and temperature sensor, every 10 seconds record in another Document the current measurement value of the device, incorporating identifiers that allow to recognize reading failures.  
In this sense, the PINs used are: 
*RTC DS3231-> Pins: 1, 3, 5, 7, 9 for 3.3V, SDA, SCL, NC, and Ground respective 
*DHT11 -> Pin: 19 for data 
*PIR -> Pin: 40 for level 
*Buzzer(alarm) -> Pin: 36 for level
===============================================================
The statement was developed by Víctor Machado - DRK Victor-DRK
