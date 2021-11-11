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
        #print(json.dumps(self.__config, indent = 4, sort_keys=True))
        self.updateShotClock(10, "white", "yellow")
        self.updateShotClock(4, "white", "yellow")
        
        
    def checkForConnection(self, ip):
        req = urllib.request.Request('http://' + str(ip) + '/API')
        try:
            urllib.request.urlopen(req, timeout=0.1)
            # print("Valid connection")
            return True
        except urllib.error.URLError:
            # print('Connection has failed. Will try again')
            return True
                
    def __setText(self, ip, id, name, value):
        try:
            url = 'http://' + str(ip) + '/API/?Function=SetText&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value)
            print(url)
            urllib.request.urlopen(url, timeout=0.1)
        except:
            return
        
    def __setTextColour(self, ip, id, name, value):
        try:
            url = 'http://' + str(ip) + '/API/?Function=SetTextColour&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value)
            print(url)
            urllib.request.urlopen(url, timeout = 0.1)
        except:
            return

    def __setTextAndColour(self, ip, id, name, value, colour):
        try:
            url = 'http://' + str(ip) + '/API/?Function=SetTextColour&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value) + \
                                             '?Function=SetText&Input=' + str(id) + '&SelectedName=' + str(name) + '&Value=' + str(value)
            print(url)
            urllib.request.urlopen(url, timeout = 0.1)
        except:
            return
    
    def changeTimeColor(self, color):
        for scoreboard in self.__config['vMix']:
            self.__setTextColour(scoreboard['ip_adres'], scoreboard['vmix_id'], scoreboard['time_seconds'], color)
            self.__setTextColour(scoreboard['ip_adres'], scoreboard['vmix_id'], scoreboard['time_minutes'], color)
            self.__setTextColour(scoreboard['ip_adres'], scoreboard['vmix_id'], scoreboard['time_spacer'], color)

    def changeShotClockColor(self, color):
        try:
            for scoreboard in self.__config['vMix']:
                self.__setTextColour(scoreboard['ip_adres'], scoreboard['vmix_id'], scoreboard['shotclock_seconds'], color)
        except:
            return
    
    def updateSeconds(self, seconds):
        try:
            for scoreboard in self.__config['vMix']:
                self.__setText(scoreboard['ip_adres'], scoreboard['vmix_id'], scoreboard['time_seconds'], seconds)
        except:
            return
        
    def updateMinutes(self, minutes):
        try:
            for scoreboard in self.__config['vMix']:
                self.__setText(scoreboard['ip_adres'], scoreboard['vmix_id'], scoreboard['time_minutes'], minutes)
        except:
            return                

    def updateShotClock(self, shotClock, activeColour, lowColour):
        try:
            for scoreboard in self.__config['vMix']:
                if shotClock > 5:
                    self.__setTextAndColour(scoreboard['ip_adres'], scoreboard['vmix_id'], scoreboard['shotclock_seconds'], shotClock, activeColour)
                else:
                    self.__setTextAndColour(scoreboard['ip_adres'], scoreboard['vmix_id'], scoreboard['shotclock_seconds'], shotClock, lowColour)
        except:
            return                

    def updateScoreHome(self, scoreHome):
        try:
            for scoreboard in self.__config['vMix']:
                self.__setText(scoreboard['ip_adres'], scoreboard['vmix_id'], scoreboard['score_home'], scoreHome)
        except:
            return                
        
    def updateScoreGuest(self, scoreGuest):
        try:
            for scoreboard in self.__config['vMix']:
                self.__setText(scoreboard['ip_adres'], scoreboard['vmix_id'], scoreboard['score_guest'], scoreGuest)
        except:
            return                

if __name__ == "__main__":
    vMixIntegration('config.JSON')