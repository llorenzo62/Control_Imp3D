# Control Imp3d
La libreria __motion__ controla la camara y la ejecución del script __movimiento__
comprobar que el usuario pi pertenece al grupo motion

movimiento hace touch en un archivo llamado __movimiento.test__ cuando __motion__ detecta movimiento

Una posible configuración para motion en motion.conf:

```
sudo cp motion.conf /etc/motion/motion.conf
```


__quietud.py__ activa la salida (12) de Raspberry y controla la diferencia de tiempo entre la hora actual y la ultima detección de movimiento por motion
Si esta diferencia es mayor que limite (minutos) desactiva la salida y termina el script

Para poder desconectarse de Rasp. ejecutar procesos en bg:


```
nohup motion -s &  
nohup python3 quietud.py &
```
