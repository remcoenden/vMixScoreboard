#####################################################################
# Python script to update scoreboard information via the vMix API
# Created by: Remco van den Enden
# Date: 09 July 2020
#####################################################################


#####################################################################
# Imports
#####################################################################
import gpiozero
import urllib.request
import time


#####################################################################
# IP-Address
#####################################################################
IP_ADDRES = "192.168.2.13:8088"

#####################################################################
# Title name definitions
#####################################################################
SCOREBOARD_ID = "825a2846-6a60-4b07-9ffb-990e3272ad4f"
SCOREBORAD_HOME_NAME = "HomeName.Text"
SCOREBOARD_GUEST_NAME = "GuestName.Text"

SCOREBOARD_SCORE_HOME = "ScoreHome.Text"
SCOREBOARD_SCORE_GUEST = "ScoreGuest.Text"

SCOREBOARD_TIME_SECONDS = "TimeSeconds.Text"
SCOREBOARD_TIME_MINUTES = "TimeMinutes.Text"
SCOREBOARD_TIME_SPACER = "Time_spacer.Text"

#####################################################################
# Pin definitions
#####################################################################
dataInputPin = 4    # GPIO4  = Pin  7
strobeInputPin = 5  # GPIO5  = Pin 29
clockD1Pin = 6      # GPIO6  = Pin 31
clockD2Pin = 12     # GPIO12 = Pin 32
clockD3Pin = 13     # GPIO13 = Pin 33
clockD4Pin = 17     # GPIO17 = Pin 11
clockD5Pin = 18     # GPIO18 = Pin 12
clockD6Pin = 22     # GPIO22 = Pin 15
clockD7Pin = 23     # GPIO23 = Pin 16
clockD8Pin = 24     # GPIO24 = Pin 18

#####################################################################
# HTML Colours
#####################################################################
INACTIVE = "red"
ACTIVE = "white"

#####################################################################
# Global variables
#####################################################################
TIME_OUT = 3 #in seconds

dataDigit1 = ""
dataDigit2 = ""
dataDigit3 = ""
dataDigit4 = ""
dataDigit5 = ""
dataDigit6 = ""
dataDigit7 = ""
dataDigit8 = ""

digit1 = -1
digit2 = -1
digit3 = -1
digit4 = -1
digit5 = -1
digit6 = -1
digit7 = -1
digit8 = -1

#####################################################################
# API Functions
#####################################################################
def checkForConenction(ip):
    req = urllib.request.Request('http://' + str(ip) + '/API')
    while True:
        try:
            urllib.request.urlopen(req)
            return
        except urllib.error.URLError:
            print('Connection has failed. Will try again in ' + str(TIME_OUT) + ' seconds.')
            time.sleep(TIME_OUT)

def setText(ip, id, name, value):
    urllib.request.urlopen('http://' + str(ip) + '/API/?Function=SetText&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value))

def setTextColour(ip, id, name, value):
    urllib.request.urlopen('http://' + str(ip) + '/API/?Function=SetTextColour&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value))
    
#####################################################################
# Input device functions
#####################################################################    
def dataToDigit(digitData):
    if len(digitData) == 8:
        if digitData == "00110000":
            return int(1)
        elif digitData == "01101110":
            return int(2)
        elif digitData == "01111010":
            return int(3)
        elif digitData == "10111000":
            return int(4)
        elif digitData == "11011010":
            return int(5)
        elif digitData == "11011110":
            return int(6)
        elif digitData == "01110000":
            return int(7)
        elif digitData == "11111110":
            return int(8)
        elif digitData == "11111010":
            return int(9)
        elif digitData == "11110110":
            return int(0)
        elif digitData == "00000000":
            return int(-1)
        else:
            return
    else:
        return
    
def mergeNumbers(first, second):
    if first == -1 and second == -1:
        return 0
    elif first == -1:
        return second
    elif second == -1:
        return first
    else:
        return (first * 10) + second
    

def newData(clockGpioNumber):
    newValue = str(dataInput.value)
    
    if clockGpioNumber.pin.number == clockD1Pin:
        global dataDigit1
        dataDigit1 = newValue + dataDigit1
        print(dataDigit1)

def strobe():
    global digit1; global dataDigit1
    
    temp = dataToDigit(dataDigit1)
    if isinstance(temp, int):
        digit1 = temp
    dataDigit1 = ""
    print(digit1)
    
    
#####################################################################
# Setup input devices
#####################################################################
## Init data pins with gpiozero libray
dataInput = gpiozero.DigitalInputDevice(dataInputPin, pull_up = None, active_state = True)
strobeInput = gpiozero.DigitalInputDevice(strobeInputPin, pull_up = None, active_state = True)
clockD1 = gpiozero.DigitalInputDevice(clockD1Pin, pull_up = None, active_state = True)

## Setup function to execute
clockD1.when_activated = newData
strobeInput.when_activated = strobe
    
#####################################################################
# Main
#####################################################################
def main():
    oldSeconds = 0
    attempt = 0
    
    oldHomeScore = 0
    oldGuestScore = 0
    
    # Test if API connection is possible
    # If not, keep trying
    checkForConenction(IP_ADDRES)
    
    while(True):        
        # Get current time
        # This should be replaced by something to read out
        # the information from the scoreboard
        currentSeconds = time.strftime("%S")
        currentMinutes = time.strftime("%M")
        
        # Check is there is an update in the seconds
        # If so, push updated seconds and minutes to vMix
        # If not, check again for 10 times over a whole second
        # If still no changes, colour the seconds, minutes and semicolon red.
        if(oldSeconds == currentSeconds):
            attempt += 1
        else:
            setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, currentSeconds)
            setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, currentMinutes)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, ACTIVE)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, ACTIVE)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SPACER, ACTIVE)
            oldSeconds = currentSeconds
            attempt = 0
            
        if(attempt > 10):
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, INACTIVE)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, INACTIVE)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SPACER, INACTIVE)
        
        # Check if there is an update in the home score
        # If so, push updated score to vMix
        homeScore = mergeNumbers(digit1, digit2)    # Change for data from the scoreboard
        if(oldHomeScore != homeScore):
            setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_SCORE_HOME, homeScore)
            oldHomeScore = homeScore
        
        # Check if there is an update in the guest score
        # If so, push updated score to vMix
        guestScore = 1    # Change for data from the scoreboard
        if(oldGuestScore != guestScore):
            setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_SCORE_GUEST, guestScore)
        
        time.sleep(0.1)
        
        
#####################################################################
# Start Program
#####################################################################
main()