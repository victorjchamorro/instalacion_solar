 
Lectura de BMS chino mediante rasberry pi, python, node-red y emoncms

Código python basado en: https://github.com/simat/BatteryMonitor

El flujo es el siguiente:

Desde Node-red se leen los valores obtenidos del ejecutable bms_nodered.sh que lanza bms_nodered.py, los procesa y los manda al emoncms

Tengo udev.rules para asignar un nombre concreto a cada USB, el script bms_nodered.py lee del puerto /dev/ttyUSB_bms, requiere ajustar los datos según el conversor USB que utilicéis:
En mi caso: ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303"

Utilizo un conversor USB-ttl para leer los datos del BMS conectado al puerto del bluetooth (no puede tener el bluetooth a la vez que el conversor USB)

