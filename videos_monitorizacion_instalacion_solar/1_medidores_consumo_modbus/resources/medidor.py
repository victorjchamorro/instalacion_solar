#!/usb/bin/python
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


def leer(addr):
    client = ModbusClient(method = 'rtu', port = '/dev/ttyUSB0', baudrate = 9600)
    client.connect()
    result = client.read_input_registers(0x0000,10,unit=addr)

    print "V:", float(result.registers[0])/10
    print "A:", float(result.registers[1])/1000
    print "W:",float(result.registers[3])/10
    print "Hz:", float(result.registers[7])/10
    print "pf:", float(result.registers[8])/100

    #Leemos el registro Hold (configuracion)
    result2 = client.read_holding_registers(0x0002, 1, unit=addr)
    print "Direccion:", result2.registers[0]

    #Guardamos registro Hold (configuracion de la direccion)
    #client.write_register(0x0002, 2, unit=1)
    client.close()
    time.sleep(1)
    print "asdf"


try:
    print "- Medidor 1"
    leer(1)
    pass
except Exception,e:
    print str(e)

try:
    print "- Medidor 2"
    leer(2)
    pass
except Exception,e:
    print str(e)
