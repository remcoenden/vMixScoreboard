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
import serial

# Setup serial port
ser = serial.Serial ("/dev/ttyS0", 9600)


#####################################################################
# IP-Address
#####################################################################
IP_ADDRES = "10.12.0.60:8088"

#####################################################################
# Title name definitions
#####################################################################
SCOREBOARD_ID = "4e64175f-2b61-4edc-92c2-b60a836effc8"
SCOREBORAD_HOME_NAME = "HomeName.Text"
SCOREBOARD_GUEST_NAME = "GuestName.Text"

SCOREBOARD_SCORE_HOME = "ScoreHome.Text"
SCOREBOARD_SCORE_GUEST = "ScoreGuest.Text"

SCOREBOARD_TIME_SECONDS = "TimeSeconds.Text"
SCOREBOARD_TIME_MINUTES = "TimeMinutes.Text"
SCOREBOARD_TIME_SPACER = "Time_spacer.Text"

MATCH_INFO_ID = "337ed5cf-ef82-4c56-825b-dcaee536e330"
MATCH_INFO_SECONDS = "Seconds.Text"
MATCH_INFO_MINUTES = "Minutes.Text"

#####################################################################
# HTML Colours
#####################################################################
INACTIVE = "red"
ACTIVE = "white"

#####################################################################
# Global variables
#####################################################################
TIME_OUT = 3 #in seconds

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

    
def mergeNumbers(first, second):
    try:
        first = int(first)
        second = int(second)
    except:
        return -1
        
    if first == -1 and second == -1:
        return "0"
    elif first == 0 and second == 0:
        return "00"
    elif first == 0 and second > 0:
        return "0" + str(second)
    elif first == -1:
        return str(second)
    elif second == -1:
        return str(first)
    else:
        return str( (first * 10) + second )    
    
#####################################################################
# Main
#####################################################################
def main():
    oldSeconds = -1
    oldMinutes = -1    
    oldHomeScore = -1
    oldGuestScore = -1
    
    attempt = 0
    makeActiveColour = True
    
    # Test if API connection is possible
    # If not, keep trying
    checkForConenction(IP_ADDRES)
    digits = [0, 0, 0, 0, 0, 0, 0, 0]
    while(True):
        lengthReceivedData = 0
        while(lengthReceivedData != 8):
            received_data = ser.readline()
            decoded_data = str(received_data[0:len(received_data)-1].decode("utf-8"))
            digits = decoded_data.split('.')
            lengthReceivedData = len(digits)
        
        
#         print(mergeNumbers(digits[0], digits[1]) + "   " + mergeNumbers(digits[2], digits[3]) + ":" + mergeNumbers(digits[4], digits[5]) + "   " + mergeNumbers(digits[6], digits[7]))
        
        # Check is there is an update in the seconds
        # If so, push updated seconds and minutes to vMix
        # If not, check again for 10 times over a whole second
        # If still no changes, colour the seconds, minutes and semicolon red.
        currentSeconds = mergeNumbers(digits[4], digits[5])
        if((oldSeconds == currentSeconds) & (oldSeconds != -1)):
            attempt += 1
        else:
            setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, currentSeconds)
            setText(IP_ADDRES, MATCH_INFO_ID, MATCH_INFO_SECONDS, currentSeconds)

            
            if(makeActiveColour):
                setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, ACTIVE)
                setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, ACTIVE)
                setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SPACER, ACTIVE)
                makeActiveColour = False;
            oldSeconds = currentSeconds
            attempt = 0
        
        currentMinutes = mergeNumbers(digits[2], digits[3])
        if((oldMinutes != currentMinutes) & (currentMinutes != -1)):
            setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, currentMinutes)
            setText(IP_ADDRES, MATCH_INFO_ID, MATCH_INFO_MINUTES, currentSeconds)
            oldMinuts = currentMinutes
        
        if(attempt > 10):
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, INACTIVE)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, INACTIVE)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SPACER, INACTIVE)
            makeActiveColour = True
        
        # Check if there is an update in the home score
        # If so, push updated score to vMix
        homeScore = mergeNumbers(digits[0], digits[1])
        if((oldHomeScore != homeScore) & (homeScore != -1)):
            setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_SCORE_HOME, homeScore)
            oldHomeScore = homeScore
        
        # Check if there is an update in the guest score
        # If so, push updated score to vMix
        guestScore = mergeNumbers(digits[6], digits[7])
        if((oldGuestScore != guestScore) & (guestScore != -1)):
            setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_SCORE_GUEST, guestScore)
        
        time.sleep(0.1)
        ser.reset_input_buffer()
        
        
#####################################################################
# Start Program
#####################################################################
main()