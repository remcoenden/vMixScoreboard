/************************************************
 * vMixScoreboard
 * Author:  Remco van den Enden
 * Date:    23 December 2020
 ***********************************************/



/************************************************
 * INCLUDES
 ***********************************************/
#include <mbed.h>


/************************************************
 * PIN DEFINITIONS
 ***********************************************/
Serial pc(PB_6, PB_7);

#define DATA_PIN      PA_7
#define STROBE_PIN    PA_5

#define CLOCK_D1_PIN  PA_2
#define CLOCK_D2_PIN  PA_4
#define CLOCK_D3_PIN  PB_1
#define CLOCK_D4_PIN  PA_3
#define CLOCK_D5_PIN  PA_6
#define CLOCK_D6_PIN  PC_14
#define CLOCK_D7_PIN  PA_0
#define CLOCK_D8_PIN  PC_15

#define POWER_LED     PA_1

// Init pins
DigitalIn data(DATA_PIN);
InterruptIn strobe(STROBE_PIN);

InterruptIn digit1(CLOCK_D1_PIN);
InterruptIn digit2(CLOCK_D2_PIN);
InterruptIn digit3(CLOCK_D3_PIN);
InterruptIn digit4(CLOCK_D4_PIN);
InterruptIn digit5(CLOCK_D5_PIN);
InterruptIn digit6(CLOCK_D6_PIN);
InterruptIn digit7(CLOCK_D7_PIN);
InterruptIn digit8(CLOCK_D8_PIN);

DigitalOut led(POWER_LED);


/************************************************
 * MAIN
 ***********************************************/
int main() {
  while(1) {
    // put your main code here, to run repeatedly:
  }
}