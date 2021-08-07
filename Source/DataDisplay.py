#####################################################################
# Python script to push scoreboard data to a vMix stream PC
# Created by: Remco van den Enden
# Date: August 3th, 2021
#####################################################################

#####################################################################
# Imports
#####################################################################
import serial
import sys

#####################################################################
# Class
#####################################################################
class DataDisplay:
    Minutes = 0
    Seconds = 0
    Home = 0
    Guest = 0
    Goal = False
    HalfSecondCount = 0
    
    def __init__(self, com):
        try:
            self.ser = serial.Serial(port = com, baudrate = 57600)
        except Exception as e:
            print(e)
            sys.exit(2)
        
    def mapSecondMinuteChar(self, byteChar):
        if byteChar == 176:
            return b'0'
        elif byteChar == 177:
            return b'1'
        elif byteChar == 178:
            return b'2'
        elif byteChar == 179:
            return b'3'
        elif byteChar == 180:
            return b'4'
        elif byteChar == 181:
            return b'5'
        elif byteChar == 182:
            return b'6'
        elif byteChar == 183:
            return b'7'
        elif byteChar == 184:
            return b'8'
        elif byteChar == 185:
            return b'9'        
    
    # To make sure the data string is read from the beginning,
    # the first char read will be check to be a '{', indicating
    # the start of a new message. The message will be discarded
    # if the first char doesn't match up.
    # The method will read until a '}' is received, indicating
    # the end of a message.
    def readScoreboardData(self):
        while True:
            self.ser.flushInput()
            try:
                rawData = self.ser.read_until(b'}')
            except:
                rawData = ''
#             print(rawData)
            # read_until returns byte data, so a conversion to string is needed
            if (chr(rawData[0]) == '{'):
                try:
                    return rawData.decode("utf-8")
                except:
#                     print('EXCEPTION')
#                     print(rawData)
                    data = rawData[:18] + self.mapSecondMinuteChar(rawData[18]) + rawData[19:]
                    return data.decode("utf-8")
            else:
                rawData = ''
                data = ''
        
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
    def getScoreboardData(self, data):
        d = dict()
        if not (data[16]== 'd' or data[16] == '+' or data[16] == 'u'):
            if not(data[17] == 'G' or data[13] == 'G'):
                Goal = False
                self.Minutes = data[17:19]
                self.Seconds = data[19:21]
            else:
                Goal = True
                
            if Goal == True:
                self.HalfSecondCount = self.HalfSecondCount + 1
                if self.HalfSecondCount % 2 == 0:
                    self.HalfSecondCount = 0
                    self.Seconds = str( int(self.Seconds) - 1 )
                    if int(self.Seconds) < 0:
                        self.Seconds = str(59)
                        self.Minutes = str( int(self.Minutes) - 1 )
                        if int(self.Minutes) < 0:
                            self.Minutes = str(0)
                
            if not (data[13] == 'G' or data[14] == 'd'):
                self.Home = data[15:17]
                self.Guest = data[13:15]
            
        d['minutes'] = self.Minutes
        d['seconds'] = self.Seconds
        d['home'] = self.Home
        d['guest'] = self.Guest 

        return d
    