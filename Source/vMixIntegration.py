#####################################################################
# Python script to push scoreboard data to a vMix stream PC
# Created by: Remco van den Enden
# Date: August 1th, 2021
#####################################################################

#####################################################################
# Imports
#####################################################################
import urllib.request
import time
import json

#####################################################################
# Class
#####################################################################
class vMixIntegration:
    __config = ''
    
    def __init__(self, configJSON):
        with open(configJSON) as f:
            __config = json.load(f)
        #print(json.dumps(__config, indent = 4, sort_keys=True))
        
        
    def checkForConnection(self, ip):
        req = urllib.request.Request('http://' + str(ip) + '/API')
        while True:
            try:
                urllib.request.urlopen(req)
                return
            except urllib.error.URLError:
                print('Connection has failed. Will try again')
                time.sleep(5)
                
    def __setText(self, ip, id, name, value):
        urllib.request.urlopen('http://' + str(ip) + '/API/?Function=SetText&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value))
        
    def __setTextColour(self, ip, id, name, value):
        urllib.request.urlopen('http://' + str(ip) + '/API/?Function=SetTextColour&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value))
        
    def updateSecond(self, seconds):
        self.__setText(__config['ip_adres'], __config['scoreboard_id'], __config['scoreboard_time_seconds'], __seconds)
        self.__setText(__config['ip_adres'], __config['match_info_id'], __config['match_info_seconds'], __seconds)
        
    def updateMinutes(self, minutes):
        self.__setText(__config['ip_adres'], __config['scoreboard_id'], __config['scoreboard_time_minutes'], __minutes)
        self.__setText(__config['ip_adres'], __config['match_info_id'], __config['match_info_minutes'], __minutes)
        
    def updateScoreHome(self, scoreHome):
        self.__setText(__config['ip_adres'], __config['scoreboard_id'], __config['scoreboard_score_home'], __scoreHome)
        self.__setText(__config['ip_adres'], __config['match_info_id'], __config['match_info_score_home'], __scoreHome)
        
    def updateScoreGuest(self, scoreGuest):
        self.__setText(__config['ip_adres'], __config['scoreboard_id'], __config['scoreboard_score_guest'], __updateScoreGuest)
        self.__setText(__config['ip_adres'], __config['match_info_id'], __config['match_info_score_guest'], __updateScoreGuest)