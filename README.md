# vMixScoreboard
[![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/tterb%2FHyde)
[![GitHub Issues](https://img.shields.io/github/issues/remcoenden/vMixScoreboard.svg)](https://github.com/remcoenden/vMixScoreboard/issues)
[![License](https://img.shields.io/badge/License-Boost%201.0-lightblue.svg)](https://www.boost.org/LICENSE_1_0.txt)

With vMixScoreboard you will be able to pull data straight from your Anatec scoreboard and push it into vMix with the use of the vMix API. All that is needed is a STM32 Blue Pill and a Raspberry Pi (for now).

## Background
About a year ago I started a livestream project for my local sports club. We wanted to give everybody the opportunity to see our top class matches, even those that live across the country. One of the major graphics showing during the game is the live score. Since we did not want to update the score and time by hand, we started looking for an automated solution. We used to use the program [Scoreboard OCR](http://scoreboard-ocr.com/) but unfortunately for us they decided to ask absurd prices for their service, so back to the drawing board it was. With some inspiration from other clubs in our league we decided to make use of a Raspberry Pi, connected to the scoreboard to get out data in vMix.

## Design overview
In this section the overall design of vMixScoreboard will be discussed, starting with the schematic overview. After that the basic functionality of the script will be discussed.

### Electrical schematic
TODO: Update Electrical schematic

After looking into our scoreboard we found that the individual segments were driven by a PIC16F873 shift register. The PIC would get 8-bits of data, pushed by a segment-specific clock. Once all eight segments were filled with new data, a strobe signal would push the data to LED-drives, which in turn would turn on the correct segments. This whole procces would take less than two thents of a millisecond and would always repeat.
Our first thought was to hook op a Raspberry Pi to the scoreboard. That way we could read the data and directly push it to vMix. After some testing we came to the conclusion that the Raspberry Pi was not suited for the job. The data lines had sush speed that the Pi could not properly read the incomming data, and thus miss clock cycles or read wrong data. That's why we integrated a STM32 Blue Pill. This microcontroller is fast enough the properly read all of the data, without errors. Because the Blue Pill doesn't have native ethernet connectivity we still needed the Raspberry Pi. The two are connected by a UART protocol. Once the Blue Pill has new data, it will push it over UART to the Raspberry where a Python script will push the data to vMix.

In the future I want to get rid of the Raspberry Pi completely and just hook op a ethernet port to the Blue Pill, but because of deadlines I haven't been able to do that jet.

Our goal is to permanently mount the Raspberry Pi and the Blue Pill in the scoreboard, so we needed a way to turn it on and off on demand. The power switch should enable this. A small piece of software is needed to use this switch. Luckely for us [HowChoo](https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi) has made an excelent tutorial about this issue. I highly reccomend you use that. The beauty of this design lays in the fact that no modification to the original scoreboard PCB is needed. Just solder the UART wire to the correct pin of the microcontroller, together with a GROUND connection and that’s it!

### Software overview
The software for vMixScoreboard is relatively easy. The main program consists of two main features: reading data from the serial connection and pushing this data to vMix via the API. 

To get a feeling for the signal we are working with I created the pictures below. The software simply reads the data and finds out with the corrosponding value is with a simple state machine. Once this value is found it is pushed to the Raspberry Pi. There I check for differences between the current data en new data. Only when these are different the new data gets pushed to vMix. This way the API doesn't have to send more data than needed.

## vMix API
This project uses the vMix API to interface the Raspberry Pi with vMix. More information about this API can be found [here](https://www.vmix.com/help19/index.htm?DeveloperAPI.html)

## Credits
This project would not be possible if it wasn't for the help, information and inspiration from the following people:
- [Jan Jaap Elenbaas](https://www.linkedin.com/in/jjelenbaas/)
- Rick Voskamp
- [André Kager](https://www.linkedin.com/in/andrekager/)

## License
Boost Software License 1.0 © [Remco van den Enden](https://github.com/remcoenden)


