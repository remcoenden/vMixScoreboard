/************************************************
 * vMixScoreboard V2
 *
 * Created by: Remco van den Enden
 * Last edited by: Remco van den Enden
 * Last edited on: Tue Jun 29 2021
************************************************/



/************************************************
 * INCLUDES
 ***********************************************/
#include <Arduino.h>

#include <ScoreboardDigit.h>

#include "debug.h"

/************************************************
 * PIN DEFINITIONS
 ***********************************************/
#define DATA_PIN      5
#define STROBE_PIN    8

#define CLOCK_D1_PIN  10
#define CLOCK_D2_PIN  11
#define CLOCK_D3_PIN  12
#define CLOCK_D4_PIN  13
#define CLOCK_D5_PIN  14
#define CLOCK_D6_PIN  15
#define CLOCK_D7_PIN  16
#define CLOCK_D8_PIN  17

#define POWER_LED     2


/************************************************
 * GLOBAL VARIABLES
 ***********************************************/


/************************************************
 * MAIN FUNCTIONS
 ***********************************************/
void setup() {
  /* Start serial debug port */
  initiateSerialDebug();

  /* Turn on power led to indicate succesfull power on */
  pinMode(POWER_LED, OUTPUT);
  digitalWrite(POWER_LED, HIGH);
}

void loop() {
  DEBUG("Hello World!");
  DEBUG_ERR("I've got an error");
  DEBUG_WARN("Warning, I'm on fire");
  DEBUG_INF("FYI, the fire is onder control");
  delay(1000);
}