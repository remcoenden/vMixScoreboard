#####################################################################
# Python script to update scoreboard information via the vMix API
# Created by: Remco van den Enden
# Date: 09 July 2020
#####################################################################


#####################################################################
# Imports
#####################################################################
import urllib.request
import time


#####################################################################
# IP-Address
#####################################################################
IP_ADDRES = "10.15.52.253:8088"

#####################################################################
# Title name definitions
#####################################################################
SCOREBOARD_ID = "f1446fc4-ec48-47fb-bfaa-c04a272ef775"
SCOREBORAD_HOME_NAME = "HomeName.Text"
SCOREBOARD_GUEST_NAME = "GuestName.Text"

SCOREBOARD_SCORE_HOME = "ScoreHome.Text"
SCOREBOARD_SCORE_GUEST = "ScoreGuest.Text"

SCOREBOARD_TIME_SECONDS = "TimeSeconds.Text"
SCOREBOARD_TIME_MINUTES = "TimeMinutes.Text"
SCOREBOARD_TIME_SPACER = "Time_spacer.Text"

#####################################################################
# Global variables
#####################################################################
TIME_OUT = 3 #in seconds

#####################################################################
# HTML Colours
#####################################################################
INACTIVE = "red"
ACTIVE = "white"


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
        homeScore = 1    # Change for data from the scoreboard
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