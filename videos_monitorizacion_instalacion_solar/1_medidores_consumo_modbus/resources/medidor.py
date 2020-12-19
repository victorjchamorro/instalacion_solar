#!/usb/bin/python

from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method = 'rtu', port = '/dev/ttyUSB0', baudrate = 9600)
client.connect()

result = client.read_input_registers(0x0000,10,unit=1)

print result.registers[0]
print result.registers[1]
print result.registers[2]
print result.registers[3]
print result.registers[4]
print result.registers[5]
print result.registers[6]
print result.registers[7]
print result.registers[8]
print result.registers[9]
 
client.close()
