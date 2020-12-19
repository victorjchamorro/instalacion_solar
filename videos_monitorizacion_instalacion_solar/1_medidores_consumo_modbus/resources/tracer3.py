from pymodbus.client.sync import ModbusSerialClient as ModbusClient
 
#client = ModbusClient(method = 'rtu', port = '/dev/ttyXRUSB0', baudrate = 115200, parity ='N')
#client = ModbusClient(method = 'rtu', port = '/dev/ttyACM0:', baudrate = 115200, parity ='N')
client = ModbusClient(method = 'rtu', port = '/dev/ttyUSB1', baudrate = 115200)
client.connect()
 
result = client.read_input_registers(0x3100,6,unit=1)

print result

solarVoltage = float(result.registers[0] / 100.0)
solarCurrent = float(result.registers[1] / 100.0)
batteryVoltage = float(result.registers[3] / 100.0)
chargeCurrent = float(result.registers[4] / 100.0)
 
# Do something with the data
 
client.close()
