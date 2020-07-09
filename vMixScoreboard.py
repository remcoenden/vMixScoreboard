#####################################################################
# Python script to update scoreboard information via the vMix API
# Created by: Remco van den Enden
# Date: 09 July 2020
#####################################################################


#####################################################################
# Imports
#####################################################################
import urllib.request as request
import time


#####################################################################
# IP-Addres
#####################################################################
IP_ADDRES = "192.168.2.13:8088"


#####################################################################
# Title name defintions
#####################################################################
SCOREBOARD_ID = "545d3747-2b2f-4c7f-8af3-ef7c823226cb"
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
RED = "red"
WHITE = "white"
BLACK = "black"


#####################################################################
# API Functions
#####################################################################
def setText(ip, id, name, value):
    request.urlopen('http://' + str(ip) + '/API/?Function=SetText&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value))

def setTextColour(ip, id, name, value):
    request.urlopen('http://' + str(ip) + '/API/?Function=SetTextColour&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value))
    
#####################################################################
# Main
#####################################################################
def main():
    oldSeconds = 0
    attempt = 0
    
    oldHomeScore = 0
    oldGuestScore = 0
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
            attempt += 1;
        else:
            setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, currentSeconds)
            setText(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, currentMinutes)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, WHITE)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, WHITE)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SPACER, WHITE)
            oldSeconds = currentSeconds
            attempt = 0;
            
        if(attempt > 10):
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SECONDS, RED)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_MINUTES, RED)
            setTextColour(IP_ADDRES, SCOREBOARD_ID, SCOREBOARD_TIME_SPACER, RED)
        
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