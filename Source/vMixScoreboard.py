#####################################################################
# Python script to update scoreboard information via the vMix API
# Created by: Remco van den Enden
# Date: August 1th, 2021
#####################################################################


#####################################################################
# Imports
#####################################################################
import sys, getopt, time
import urllib.request

from vMixIntegration import vMixIntegration
from DataDisplay.python.DataDisplay import DataDisplay
from AnatecIndor.AnatecIndor import AnatecIndor

#####################################################################
# Global variables
#####################################################################
acceptedManufacturers = ["DataDisplay", "AnatecIndor"]

scoreboard = ''

#####################################################################
# Functions
#####################################################################
def validateManufacturer(manufacturer):
    if not manufacturer in acceptedManufacturers:
        raise Exception ("This manufacturer isn't supported right now" )

def setupScoreboard(manufacturer, com):
    if manufacturer == acceptedManufacturers[0]:
        scoreboard = DataDisplay(com)
        return scoreboard
    elif manufacturer == acceptedManufacturers[1]:
        scoreboard = AnatecIndor(com)
        return scoreboard

    
#####################################################################
# Main
#####################################################################
def main(argv):
    scoreboardManufacturer = ''
    configJSON = ''
    com = ''
    
    # Make sure the needed command line parameters are present
    # If these are not present, the program is unable to function and an exception is thrown
    try:
        opts, args = getopt.getopt(argv, "hm:j:c:", ["help", "manufacturer=", "config=", "com="])
        if not len(argv) > 1:
            raise Exception
    except:
        print("vMixScoreboard.py -m <", *acceptedManufacturers,  "> -j < vMixConfig.JSON > -c < COM port >")
        sys.exit(2)
        
    # Map the command line parameters to the appropriate local variable
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("vMixScoreboard.py -m <", *acceptedManufacturers,"> -j < vMixConfig.JSON > -c < COM port >")
            sys.exit()
        elif opt in ("-m", "--manufacturer"):
            scoreboardManufacturer = arg
        elif opt in ("-j", "--config"):
            configJSON = arg
        elif opt in ("-c", "--com"):
            com = arg
    
    # Check if the command line arguments are valid
    # The program is unable to function with incorrect parameters and an exception is thrown
    try:
        vMix = vMixIntegration(configJSON)
        validateManufacturer(scoreboardManufacturer)
        scoreboard = setupScoreboard(scoreboardManufacturer, com)
    except Exception as e:
        print(e)
        sys.exit(2)
    
    
    print("Scoreboard manufacturer is: ", scoreboardManufacturer)
    print("JSON config file is: ", configJSON)
    print("The seleted com port is: ", com)
    
    minutesOld = ''
    secondsOld = ''
    homeOld = ''
    guestOld = ''
    shotClockOld = ''
    update = 0
    
    vMix.changeTimeColor("White")
    
    while True:
        dataString = scoreboard.readScoreboardData()
        data = scoreboard.getScoreboardData(dataString)
        print(data.get('minutes') + ":" + data.get('seconds') + "  " + data.get('shotClock') + "    " + data.get('home') + "-" + data.get('guest'))
        
        if not minutesOld == data.get('minutes'):
            vMix.updateMinutes(data.get('minutes').strip())
            minutesOld = data.get('minutes')
            
        if not secondsOld == data.get('seconds'):
            vMix.updateSeconds(data.get('seconds').strip())
            secondsOld = data.get('seconds')
            
        if not homeOld == data.get('home'):
            vMix.updateScoreHome(data.get('home').strip())
            homeOld = data.get('home')
            
        if not guestOld == data.get('guest'):
            vMix.updateScoreGuest(data.get('guest').strip())
            guestOld = data.get('guest')
            
        if not shotClockOld == data.get('shotClock'):
            vMix.updateShotClock(data.get('shotClock').strip(), "white", "yellow")
            shotClockOld = data.get('shotClock')
    
#####################################################################
# Start program
#####################################################################
if __name__ == "__main__":
    main(sys.argv[1:])