# vMixScoreboard
[![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/tterb%2FHyde)
[![GitHub Issues](https://img.shields.io/github/issues/remcoenden/vMixScoreboard.svg)](https://github.com/remcoenden/vMixScoreboard/issues)
[![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)
[![License](https://img.shields.io/badge/License-Boost%201.0-lightblue.svg)](https://www.boost.org/LICENSE_1_0.txt)

With vMixScoreboard you will be able to pull data straight from your Anatec scoreboard and push it into vMix with the use of the vMix API. All that is needed is a Raspberry Pi connected to the serial data line of your scoreboard.

## Background
About a year ago I started a livestream project for my local sports club. We wanted to give everybody the opportunity to see our top class matches, even those that live across the country. One of the major graphics showing during the game is the live score. Since we did not want to update the score and time by hand, we started looking for an automated solution. We used to use the program [Scoreboard OCR](http://scoreboard-ocr.com/) but unfortunately for us they decided to ask absurd prices for their service, so back to the drawing board it was. With some inspiration from other clubs in our league we decided to make use of a Raspberry Pi, connected to the scoreboard to get out data in vMix.

## vMix API
This project uses the vMix API to interface the Raspberry Pi with vMix. More information about this API can be found [here](https://www.vmix.com/help19/index.htm?DeveloperAPI.html)

## License
Boost Software License 1.0 © [Remco van den Enden](https://github.com/remcoenden)


