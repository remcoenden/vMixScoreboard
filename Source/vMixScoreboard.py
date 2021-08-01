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
import time
import serial
   
    
#####################################################################
# Main
#####################################################################
def main(argv):
    scoreboardManufacturer = ''
    configJSON = ''
    com = ''
    try:
        opts, args = getopt.getopt(argv, "hm:j:c:", ["help", "manufacturer=", "config=", "com="])
    except getopt.GetoptError:
        print("vMixScoreboard.py -m <Anatec / DataDisplay> -j <vMixConfig.JSON> -c <COM port>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("vMixScoreboard.py -m <Anatec / DataDisplay> -j <vMixConfig.JSON> -c <COM port>")
            sys.exit()
        elif opt in ("-m", "--manufacturer"):
            scoreboardManufacturer = arg
        elif opt in ("-j", "--config"):
            configJSON = arg
        elif opt in ("-c", "--com"):
            com = arg
    print("Scoreboard manufacturer is: ", scoreboardManufacturer)
    print("JSON config file is: ", configJSON)
    print("The seleted com port is: ", com)
                                
    
#####################################################################
# Start program
#####################################################################
if __name__ == "__main__":
    main(sys.argv[1:])