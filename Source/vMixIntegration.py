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
            self.__config = json.load(f)
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
        try:
#             print('http://' + str(ip) + '/API/?Function=SetText&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value))
            urllib.request.urlopen('http://' + str(ip) + '/API/?Function=SetText&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value))
        except:
            return
        
    def __setTextColour(self, ip, id, name, value):
        try:
            urllib.request.urlopen('http://' + str(ip) + '/API/?Function=SetTextColour&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value))
        except:
            return
        
    def updateSeconds(self, seconds):
        self.__setText(self.__config['ip_adres'], self.__config['scoreboard_id'], self.__config['scoreboard_time_seconds'], seconds)
#         self.__setText(self.__config['ip_adres'], self.__config['match_info_id'], self.__config['match_info_seconds'], seconds)
        
    def updateMinutes(self, minutes):
        self.__setText(self.__config['ip_adres'], self.__config['scoreboard_id'], self.__config['scoreboard_time_minutes'], minutes)
#         self.__setText(self.__config['ip_adres'], self.__config['match_info_id'], self.__config['match_info_minutes'], minutes)
        
    def updateScoreHome(self, scoreHome):
        self.__setText(self.__config['ip_adres'], self.__config['scoreboard_id'], self.__config['scoreboard_score_home'], scoreHome)
#         self.__setText(self.__config['ip_adres'], self.__config['match_info_id'], self.__config['match_info_score_home'], scoreHome)
        
    def updateScoreGuest(self, scoreGuest):
        self.__setText(self.__config['ip_adres'], self.__config['scoreboard_id'], self.__config['scoreboard_score_guest'], scoreGuest)
#         self.__setText(self.__config['ip_adres'], self.__config['match_info_id'], self.__config['match_info_score_guest'], updateScoreGuest)