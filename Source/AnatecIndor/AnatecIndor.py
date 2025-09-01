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
class AnatecIndor:
    Minutes = 0
    Seconds = 0
    ShotClock = 0
    Home = 0
    Guest = 0
    Goal = False
    HalfSecondCount = 0
    
    def __init__(self, com):
        try:
            self.ser = serial.Serial(port = com, baudrate = 2400)
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
        while True:
            self.ser.flushInput()
            # Read up to the final byte of the previous message.
            # This makes sure the next message will be received as whole.
            emptyBuffer = self.ser.read_until(b'\r')
            rawData = self.ser.read_until(b'\r')
            if len(rawData) == 23:
                try:
                    return rawData.decode("utf-8")
                except:
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
    def getScoreboardData(self, data):
        d = dict()
        
        self.Minutes = data[19:21]
        self.Seconds = data[14] + data[13]
        self.ShotClock = data[0:2]
        self.Home = data[17:19]
        self.Guest = data[11] + data[10]
            
        d['minutes'] = self.Minutes
        d['seconds'] = self.Seconds
        d['shotClock'] = self.ShotClock
        d['home'] = self.Home
        d['guest'] = self.Guest 

        return d
    