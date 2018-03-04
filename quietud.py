
import os,time,sys,getopt, RPi.GPIO as GPIO
from random import randint
#Valores por defecto

limite,tmin,tmax,pin,okdebug=[2,3,30,12,False]
instrucc='''pyton3 quietud.py [-l valor -i valor -a valor -p valor]
-l: tiempo en minutos para considerar que no hay movimiento, por defecto 2
-i: tiempo minimo en segundos para comprobar si hay movimiento, por defecto 3
-a: tiempo maximo en segundos para comprobar si hay movimiento, por defecto 30
-p: numero del pin de salida de Raspberry. notacion BOARD, por defecto 12
-d: si se imprime informacion de depuracion, por defecto no
'''

try:
	opts,args=getopt.getopt(sys.argv[1:],'hdl:i:a:p:')
except:
	print(intrucc)
	sys.exit(2)

for opt,arg in opts:
	if opt=='-h':
		print(instrucc)
		sys.exit()
	elif opt in ('-i'):
		tmin=int(arg)
	elif opt in ('-a'):
		tmax=int(arg)
	elif opt in ('-l'):
		limit=int(arg)
	elif opt in ('-p'):
		pin=int(arg)
	elif opt in ('-d'):
		okdebug=True




dt=0

#Setup Raspberry
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin,GPIO.OUT)
GPIO.output(pin,GPIO.HIGH)


while dt<limite:
	#Espera un num. de segundos aleatorio: evitar periodicidades
	time.sleep(randint(tmin,tmax))

	#lee timestamp de movimiento.test
	aux=os.popen('ls -l /home/pi/mov*test').read()
	mov=[int(item) for item in aux.split()[7].split(':')]
	if okdebug:
		print(mov)

	#timestamp actual
	now=[time.localtime().tm_hour, time.localtime().tm_min]
	if okdebug:
		print(now)

	#calcula diferencia en minutos
	dt=((now[0]-mov[0])*60+(now[1]-mov[1]))
	if okdebug:
		print(dt)

#Al menos limite minutos sin movimiento
GPIO.output(pin,GPIO.LOW)
GPIO.cleanup()
