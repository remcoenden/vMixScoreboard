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
The software for vMixScoreboard is relatively easy. The main program consists of two main features: reading data from the serial connection and pushing this data to vMix via the API. The flow of this program is given in the image below.

TODO: Add Flow Diagram

The UART readout gives a string containing 54 unique characters, each representing a different digit for the scoreboard. Since this self-made protocol is used for various scoreboards with each various feature there will the characters that are of no use for us. Below you can find a list of all 54 characters and their representation.

|     Code in the frame | Meaning                                |    |     Code in the frame | Meaning                                |
|----------------------:|:---------------------------------------|----|----------------------:|:---------------------------------------|
|                     0 | START CODE = "F8"                      |    |                    27 | HOME: Individual fouls player 6        |
|                     1 | SPORT CODE = "33"                      |    |                    28 | HOME: Individual fouls player 7        |
|                     2 | "20"                                   |    |                    29 | HOME: Individual fouls player 8        |
|                     3 | Ball possession                        |    |                    30 | HOME: Individual fouls player 9        |
|                 **4** | **Timer (digit 1)**                    |    |                    31 | HOME: Individual fouls player 10       |
|                 **5** | **Timer (digit 2)**                    |    |                    32 | HOME: Individual fouls player 11       |
|                 **6** | **Timer (digit 3)**                    |    |                    33 | HOME: Individual fouls player 12       |
|                 **7** | **Timer (digit 4)**                    |    |                    34 | GUEST: Individual fouls player 1       |
|                 **8** | **HOME: Points (digit 1)**             |    |                    35 | GUEST: Individual fouls player 2       |
|                 **9** | **HOME: Points (digit 2)**             |    |                    36 | GUEST: Individual fouls player 3       |
|                    10 | HOME: Points (digit 3)                 |    |                    37 | GUEST: Individual fouls player 4       |
|                **11** | **GUEST: Points (digit 1)**            |    |                    38 | GUEST: Individual fouls player 5       |
|                **12** | **GUEST: Points (digit 2)**            |    |                    39 | GUEST: Individual fouls player 6       |
|                    13 | GUEST: Points (digit 3)                |    |                    40 | GUEST: Individual fouls player 7       |
|                    14 | Period                                 |    |                    41 | GUEST: Individual fouls player 8       |
|                    15 | HOME: Team fouls                       |    |                    42 | GUEST: Individual fouls player 9       |
|                    16 | GUEST: Team fouls                      |    |                    43 | GUEST: Individual fouls player 10      |
|                    17 | HOME: Number of time-outs              |    |                    44 | GUEST: Individual fouls player 11      |
|                    18 | GUEST: Number of tie-outs              |    |                    45 | GUEST: Individual fouls player 12      |
|                    19 | Horn                                   |    |                    46 | Time-out timer (digit 2)               |
|                **20** | **Timer start/stop**                   |    |                    47 | Time-out timer (digit 3)               |
|                    21 | Time-out timer (digit 1)               |    |                    48 | 24" Timer (digit 1)                    |
|                    22 | HOME: Individual fouls player 1        |    |                    49 | 24" Timer (digit 2)                    |
|                    23 | HOME: Individual fouls player 2        |    |                    50 | 24" Horn                               |
|                    24 | HOME: Individual fouls player 3        |    |                    51 | 24" Timer start/stop                   |
|                    25 | HOME: Individual fouls player 4        |    |                    52 | 24" display                            |
|                    26 | HOME: Individual fouls player 5        |    |                    53 | "0D"                                   |

The digits printed with **bold** are the ones that are interesting for us. These tell us exactly what the scoreboard displays regarding the time and score. The Python script will extract these precise digits from the total string so we can push them to vMix.

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


