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
    def readScoreboardData(self):
        data = ''
        while True:
            rawData = read_until('}')
            # read_until returns byte data, so a conversion to string is needed
            rawData = rawData.decode("utf-8")
            if (rawData[0] == '{') and (rawData[-1:] == '}'):
                data = rawData
                break
            else:
                rawData = ''
        
    # The whole raw data message should be 31 bytes long
    # The messages containts both the time and score, long with some
    # other random stuff that is not needed for this application
    # Counting from the first byte received, starting at 0, the data
    # is stored in the following bytes:
    #     Minutes: 17 & 18
    #     Seconds: 19 & 20
    #     Home:    13 & 14  TODO: Needs to be checked
    #     Guest:   15 & 16  TODO: Needs to be checked
    # Most of these bytes are plain ASCII, with the exception of the
    # second minute byte. A look-up tables needs to be used to read
    # that one out.
    def getScoreboardData(self, rawData):
        d = dict()
        
        d['seconds'] = rawData[19:21]
        d['home'] = rawData[13:15]
        d['guest'] = rawData[15:17]
        
        # To get the second minutes digit, the last bit of the ASCII
        # char needs to be fliped. This can be done with a XOR operation
        # To do this, the string is converted to a ASCII int representetive
        # which can be used for bitwise operations
        temp = ord(rawData[18])
        temp = chr(temp ^ 1)
        d['minutes'] = rawData[17] + temp
        return d
    