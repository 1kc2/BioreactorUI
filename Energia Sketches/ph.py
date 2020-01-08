import serial
import serial.tools.list_ports
import time

def list_available_ports():
    return [x[0] for x in list(serial.tools.list_ports.comports())]

port = list_available_ports()[1]
print(port)
ser = serial.Serial(port=port, baudrate=9600)
while True:
    ser.write('<ph,7.00>'.encode())
    time.sleep(0.2)
