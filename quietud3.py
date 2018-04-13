
import os,time, RPi.GPIO as GPIO
from random import randint



def modificaStatus(pinProg):
	'''
	Funcion callback para el control del pulsador
	y cambio de estado del Pi
	'''
	global status
	global pinLED

	GPIO.output(pinLED[status],GPIO.LOW)
	status=(status+1) % 3
	GPIO.output(pinLED[status],GPIO.HIGH)
	if status:
		dt=0
		GPIO.output(pin3D,GPIO.LOW)
		os.system('/home/pi/movimiento')
		aux=[item for item in os.popen('ps aux|grep motion') if not 'grep' in item]
		if not len(aux):
			os.system('nohup motion -c /home/pi/motion_auto.conf &')
	else:
		GPIO.output(pin3D,GPIO.HIGH)
		GPIO.output(pinPi,GPIO.LOW)


#Definicion de pines

#Reles: logica inversa
pin3D=12 #Control impresora: LOW si se detecta mov en tiempo lim; HIGH si no se detecta movimiento
pinPi=11 #autocontrol alimentacion

#Señal programador/pulsador
pinProg=29

#Control LED-RGB
pinRed=7
pinGreen=5
pinBlue=3
pinLED=[pinRed,pinGreen,pinBlue]


status=0 #Estado de Pi
dt=0 #tiempo desde el ultimo movimiento detectado, minutos
limite=5 #minutos
okdebug= False #True #imprime informacion de depuracion


GPIO.setmode(GPIO.BOARD)
for pin in [pin3D,pinPi,pinRed,pinGreen,pinBlue]:
	GPIO.setup(pin,GPIO.OUT)
GPIO.setup(pinProg,GPIO.IN)

#activa el rele Pi
GPIO.output(pinPi,GPIO.LOW)
#desactiva el rele 3D
GPIO.output(pin3D,GPIO.HIGH)
#Indica el estado Pi
GPIO.output(pinLED[status],GPIO.HIGH)

#Deteccion del pulsador mediante callback
GPIO.add_event_detect(pinProg, GPIO.RISING, callback=modificaStatus, bouncetime=200)
#GPIO.add_event_callback(pinProg, modificaStatus)#, bouncetime=200)
while True: #bucle infinito,sale con Ctrl-C
	try:
		if okdebug:
			print('Status: ',status)
		if status:
			aux=os.popen('ls -l /home/pi/mov*test').read()
			mov=[int(item) for item in aux.split()[7].split(':')]

			now=[time.localtime().tm_hour, time.localtime().tm_min]
			#por si se cruza la medianoche
			if now[0]<mov[0]:
				now[0]+=24

			dt=((now[0]-mov[0])*60+(now[1]-mov[1]))

			if okdebug:
				print('test: {} now: {} dt: {}'.format(':'.join([str(item) for item in mov]),':'.join([str(item) for item in now]),dt))
			if dt>=limite:

				GPIO.output(pin3D,GPIO.HIGH)
				if status==2:
					GPIO.output(pinPi,GPIO.HIGH)
				GPIO.output(pinLED[status],GPIO.LOW)
				status=0
				GPIO.output(pinLED[status],GPIO.HIGH)
	except:
		break

GPIO.cleanup()
