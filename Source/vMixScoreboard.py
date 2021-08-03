#####################################################################
# Python script to update scoreboard information via the vMix API
# Created by: Remco van den Enden
# Date: August 1th, 2021
#####################################################################


#####################################################################
# Imports
#####################################################################
import sys, getopt

from vMixIntegration import vMixIntegration

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
        validateManufacturer(scoreboardManufacturer)
    except Exception as e:
        print(e)
        sys.exit(2)
        
    vMix = vMixIntegration(configJSON)
    
    
    print("Scoreboard manufacturer is: ", scoreboardManufacturer)
    print("JSON config file is: ", configJSON)
    print("The seleted com port is: ", com)
                                
    
#####################################################################
# Start program
#####################################################################
if __name__ == "__main__":
    main(sys.argv[1:])