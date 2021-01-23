/************************************************
 * vMixScoreboard_V2
 * Author:  Remco van den Enden
 * Date:    29 December 2020
 ***********************************************/


/************************************************
 * LIBRARIES
 ***********************************************/
/* Library from the Adruino framework */
#include <Arduino.h>

/* Standard C or C++ libraries */
#include <cstdlib>

/* Custom project libraries */
#include <vMix_interface.h>


/************************************************
 * IO PIN DEFINES
 ***********************************************/
#define SPI_CHIP_SELECT     ( PA4 )


/************************************************
 * Creation of components
 ***********************************************/
vMix_interface vmix(SPI_CHIP_SELECT);

/************************************************
 * Arduino main program
 ***********************************************/
/* Signle execution code goes here */
void setup () {
    
}

/* Intinate execution code goes here */
void loop() {

}