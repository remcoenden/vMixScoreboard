#####################################################################
# Python script to update scoreboard information via the vMix API
# Created by: Remco van den Enden
# Date: August 1th, 2021
#####################################################################


#####################################################################
# Imports
#####################################################################
import sys, getopt
import urllib.request

from vMixIntegration import vMixIntegration
from DataDisplay import DataDisplay

#####################################################################
# Global variables
#####################################################################
acceptedManufacturers = ["DataDisplay"]

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
    update = 0
    
    while True:
        dataString = scoreboard.readScoreboardData()
        data = scoreboard.getScoreboardData(dataString)
        
        if not minutesOld == data.get('minutes'):
            vMix.updateMinutes(data.get('minutes').strip())
            minutesOld = data.get('minutes')
            update = 1
            
        if not secondsOld == data.get('seconds'):
            vMix.updateSeconds(data.get('seconds').strip())
            secondsOld = data.get('seconds')
            update = 1
            
        if not homeOld == data.get('home'):
            vMix.updateScoreHome(data.get('home').strip())
            homeOld = data.get('home')
            update = 1
            
        if not guestOld == data.get('guest'):
            vMix.updateScoreGuest(data.get('guest').strip())
            guestOld = data.get('guest')
            update = 1
            
        if update == 1:
            update = 0
            #https://vstats.app/sbo/?min=JJ&sec=02&hsc=11&asc=12
            url = "https://vstats.app/sbo/?min=" + data.get('minutes').strip() + \
                  "&sec="+ data.get('seconds').strip() + \
                  "&hsc=" + data.get('home').strip() + \
                  "&asc=" + data.get('guest').strip()
            try:
                urllib.request.urlopen(url, timeout=1)
            except:
                # Failed to push to vStats
                # Keep update = 1 to make sure we try again on the next loop
                update = 1
            
            #update naar server API   data.get('seconds').strip() data.get('home').strip() data.get('guest').strip()
            printFormat = "Time: {0:>2}:{1:<8} Score: {2:>2}-{3:<2}"
            print(printFormat.format(data.get('minutes'),
                                     data.get('seconds'),
                                     data.get('home'),
                                     data.get('guest') ) )
                                
    
#####################################################################
# Start program
#####################################################################
if __name__ == "__main__":
    main(sys.argv[1:])