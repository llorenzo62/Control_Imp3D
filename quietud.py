
import os,time, RPi.GPIO as GPIO
from random import randint

pin=12 #pin de salida rasp.pi: HIGH si se detecta mov en tiempo lim; LOW si no se detecta movimiento
dt=0 #tiempo desde el ultimo movimiento detectado, minutos
limite=2 #minutos
okdebug=False # True imprime informacion de depuracion

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin,GPIO.OUT)

GPIO.output(pin,GPIO.HIGH)

while dt<limite:
	time.sleep(randint(2,30)) #evitar mov. periodicos

	aux=os.popen('ls -l /home/pi/mov*test').read()
	mov=[int(item) for item in aux.split()[7].split(':')]
	if okdebug:
		print(mov)
	now=[time.localtime().tm_hour, time.localtime().tm_min]
	if okdebug:
		print(now)
	dt=((now[0]-mov[0])*60+(now[1]-mov[1]))

	if okdebug:
		print(dt)
GPIO.output(pin,GPIO.LOW)
GPIO.cleanup()
