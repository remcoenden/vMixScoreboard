# vMixScoreboard
[![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/tterb%2FHyde)
[![GitHub Issues](https://img.shields.io/github/issues/remcoenden/vMixScoreboard.svg)](https://github.com/remcoenden/vMixScoreboard/issues)
[![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)
[![License](https://img.shields.io/badge/License-Boost%201.0-lightblue.svg)](https://www.boost.org/LICENSE_1_0.txt)

With vMixScoreboard you will be able to pull data straight from your Anatec scoreboard and push it into vMix with the use of the vMix API. All that is needed is a Raspberry Pi connected to the serial data line of your scoreboard.

## Background
About a year ago I started a livestream project for my local sports club. We wanted to give everybody the opportunity to see our top class matches, even those that live across the country. One of the major graphics showing during the game is the live score. Since we did not want to update the score and time by hand, we started looking for an automated solution. We used to use the program [Scoreboard OCR](http://scoreboard-ocr.com/) but unfortunately for us they decided to ask absurd prices for their service, so back to the drawing board it was. With some inspiration from other clubs in our league we decided to make use of a Raspberry Pi, connected to the scoreboard to get out data in vMix.

## Design overview
In this section the overall design of vMixScoreboard will be discussed, starting with the schematic overview. After that the basic functionality of the Python script will be discussed.

### Electrical schematic
Below you can find the electrical schematic design to hook up the Raspberry Pi to the scoreboard. I have tested this design with a Raspberry Pi 4 and a PIC16F873 driving the scoreboard. I do not know if this schematics still works for different scoreboards driven by different microcontroller, but the same basic principal should apply.
Our goal is to permanently mount the Raspberry Pi in the scoreboard, so we needed a way to turn it on and off on demand. The power switch should enable this. A small piece of software is needed to use this switch, but more about that later on (TODO: add software for power switch).

![Electrical Schematic](https://github.com/remcoenden/vMixScoreboard/blob/master/vMixScoreboard%20Schematic.png "Schematic design")

The beauty of this design lays in the fact that no modification to the original scoreboard PCB is needed. Just solder the UART wire to the correct pin of the microcontroller, together with a GROUND connection and that’s it!

### Software overview
The software for vMixScoreboard is relatively easy. The main program consists of two main features: reading data from the serial connection and pushing this data to vMix via the API. 

The UART string coming from the PIC16F873 is of variable length and can have three main states, one for updating the time, one for updating the score and finally one for updating the period. Each of these states in indicated with a different header. Below you can find an example showing each state.

#### Time update
An time update is given as follows

```
??RD! 2500\n
??RD! 2459\n
??RD! 2458\n
```

Where the initial time of *25:00* counts down with one second.

#### Score update
An score update is given as follows

```
??RD#  0  0 \n
??RD#  1  0 \n
??RD#  1  1 \n
??RD# 10  10\n
```

Here to initial score starts at 0 - 0 (HOME - GUEST). After that +1 is added for HOME, the same is done for GUEST. Once the score reaches double digits the position of the scores within the string changes a bit. Please note that the score for HOME and GUEST are always separated by two `spaces`.

#### Period update
Finally there is the period update. This is indicated as follows

```
??RD% 1\n
??RD! 2\n
```

Where the first line indicated the first period and the second line the second period.

#### Flow diagram
The next step is setting up a Python script so we can read the data coming from the PIC16F873 and extract the useful data from it. 

---

The power button works by shorting GPIO3 to GROUND, basicly exactly the same as the power button on your computer. This function is not included out of the box on your Raspberry Pi, so a small script has to be added in order for this to work. I have followed [this](https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi) tutorial from *howchoo* to add this function to the project.

## vMix API
This project uses the vMix API to interface the Raspberry Pi with vMix. More information about this API can be found [here](https://www.vmix.com/help19/index.htm?DeveloperAPI.html)

## Credits
This project would not be possible if it wasn't for the help, information and inspiration from the following people:
- [Jan Jaap Elenbaas](https://www.linkedin.com/in/jjelenbaas/)
- Rick Voskamp
- [André Kager](https://www.linkedin.com/in/andrekager/)

## License
Boost Software License 1.0 © [Remco van den Enden](https://github.com/remcoenden)


