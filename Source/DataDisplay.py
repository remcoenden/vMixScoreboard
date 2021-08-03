#####################################################################
# Python script to push scoreboard data to a vMix stream PC
# Created by: Remco van den Enden
# Date: August 3th, 2021
#####################################################################

#####################################################################
# Imports
#####################################################################
import serial

#####################################################################
# Class
#####################################################################
class DataDisplay:
    self.ser = ''
    
    def __init__(self, com):
        try:
            self.ser = serial(port = com, baudrate = 57600)
            open()
        except Exception as e:
            print(e)
            sys.exit(2)
            
    # To make sure the data string is read from the beginning,
    # the first char read will be check to be a '{', indicating
    # the start of a new message. The message will be discarded
    # if the first char doesn't match up.
    # The method will read until a '}' is received, indicating
    # the end of a message.
    def read(self):
        data = ''
        while True:
            rawData = read_until('}')
            # read_until returns byte data, so a conversion to string is needed
            rawData = rawData.decode("utf-8")
            if (rawData[0] == '{') and (rawData[-1:] == '}'):
                data = rawData
                break
            rawData = ''
            
            
        
            