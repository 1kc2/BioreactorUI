import serial, Utilities
import serial.tools.list_ports
from Constants import *
from time import time
from glob import glob #access linux and mac os file structure hierarchy
from sys import platform #get the platform of the user's device

def list_available_ports():
    return [x[0] for x in list(serial.tools.list_ports.comports())]

class SerialPort(serial.Serial):
    def __init__(self, port='/dev/ttyACM0', baud_rate=9600, **kwargs):
        super().__init__(port, baudrate=baud_rate, **kwargs)
        self.running, self.reading_value = True, False
        self.start_time = time()
        self.time_elapsed = 0

    def open_port(self):
        if not self.isOpen():
            self.close()
            self.open()
            
    def convert(self, value):
        try:
            value = float(value)
            return value, True
        except ValueError: #has never actually been thrown
            error_msg('Conversion error',
                      'Could not convert "{}" into float.'.format(value))
            return value, False

    def read_data(self):
        '''
        A message from the board is of the format: <subsystem,value>
        with <, > indicating the start and end of data
        '''
        buffer = ""
        first_char = self.read(1) #read first byte
        #chosen character to mark start of data
        if first_char == b'<' and not self.reading_value:
            self.reading_value = True
            while self.in_waiting and self.reading_value: #while there is data to be read
                one_byte = self.read(1)
                if one_byte == b'>':
                    self.reading_value = False
                    return buffer
                #rare occurence when two messages read as one
                elif one_byte == b'<':
                    self.reading_value = False
                    return buffer
                else:
                    buffer += one_byte.decode('utf-8')
            #if it exits while loop w/o returning not all data was read
        if len(buffer) > 0: pass#print(buffer) #if not all data was read
        self.reading_value = False
        return None

    '''
    Somtimes the first few characters aren't sent so we do not start reading
    until the marker (<) is read first - end of data is marked by '>'
    With the builtin read functions, sometimes not all of the data is read,
    causing errors instead read one byte until undesirable character is found
    Test by continually running
    '''

    def read_value(self):
        try:
            msg_digest, datatype, value = None, None, None
            msg_digest = self.read_data()
            if msg_digest is not None:
                split_msg = msg_digest.split(',')
                if len(split_msg) == 2:
                    datatype, value = split_msg
                    value, converted = self.convert(value)
                    if converted:
                        elapsed_time = time() - self.start_time
                        return datatype, round(value, 1), elapsed_time
            return None, None, None
        except serial.serialutil.SerialException:
            self.running = False
            Utilities.error_msg('Disconnected', 'The MSP board was disconnected')
            return False, False, False

    def send_data(self, msg=''):
        if not msg.startswith('<'): #wrap our message with start and stop markers
            msg = '<' + msg
        if msg[-1] != '>':
            msg += '>'
        #encoded_msg = bytes(msg)
        encoded_msg = msg.encode() #convert msg into bytes to send
        self.write(encoded_msg)
        
    def close(self):
        #send message to board to stop while loop in energia sketch
        #self.send_data('stop') #fix
        self.close()

