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
    if first == -1 and second == -1:
        return 0
    elif first == -1:
        return second
    elif second == -1:
        return first
    else:
        return (first * 10) + second    
    
#####################################################################
# Main
#####################################################################
def main():
    oldSeconds = -1
    attempt = 0
    
    oldHomeScore = -1
    oldGuestScore = -1
    
    # Test if API connection is possible
    # If not, keep trying
#     checkForConenction(IP_ADDRES)
    
    while(True):        
        received_data = ser.readline()
        received_data.decode()
        received_data = str(received_data[:-1])
        print(received_data)
        split_data = received_data.split('.')
        print(split_data[0])
        
#         # Check is there is an update in the seconds
#         # If so, push updated seconds and minutes to vMix
#         # If not, check again for 10 times over a whole second
#         # If still no changes, colour the seconds, minutes and semicolon red.
#         if(oldSeconds == currentSeconds):
#             attempt += 1
#         else:
#             setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, currentSeconds)
#             setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, currentMinutes)
#             setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, ACTIVE)
#             setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, ACTIVE)
#             setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SPACER, ACTIVE)
#             oldSeconds = currentSeconds
#             attempt = 0
#             
#         if(attempt > 10):
#             setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, INACTIVE)
#             setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, INACTIVE)
#             setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SPACER, INACTIVE)
#         
#         # Check if there is an update in the home score
#         # If so, push updated score to vMix
#         homeScore = mergeNumbers(digit1, digit2)    # Change for data from the scoreboard
#         if(oldHomeScore != homeScore):
#             setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_SCORE_HOME, homeScore)
#             oldHomeScore = homeScore
#         
#         # Check if there is an update in the guest score
#         # If so, push updated score to vMix
#         guestScore = mergeNumbers(digit7, digit8)    # Change for data from the scoreboard
#         if(oldGuestScore != guestScore):
#             setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_SCORE_GUEST, guestScore)
        
        time.sleep(0.1)
        
        
#####################################################################
# Start Program
#####################################################################
main()