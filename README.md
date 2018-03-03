# Control Imp3d
La libreria __motion__ controla la camara y la ejecución del script __movimiento__  
comprobar que el usuario _pi_ pertenece al grupo _motion_

__movimiento__ hace _touch_ en un archivo llamado
_movimiento.test_ cuando __motion__ detecta movimiento

Una posible configuración para __motion__ en _motion.conf_:  

```
sudo cp motion.conf /etc/motion/motion.conf
```


__quietud.py__ activa (HIGH) la salida (12) de Raspberry y controla la diferencia de tiempo entre la hora actual y la ultima detección de movimiento por __motion__
Si esta diferencia es mayor que _limite_ (minutos) desactiva (LOW) la salida y termina el script

Para poder desconectarse de Rasp. ejecutar procesos en bg:


```
nohup motion -s &  
nohup python3 quietud.py &
```
