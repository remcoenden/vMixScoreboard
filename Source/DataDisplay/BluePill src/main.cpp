/************************************************
 * vMixScoreboard
 * Author:  Remco van den Enden
 * Data:    26 August 2020
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


/**********************************************************************
 * GLOBAL VARIABLES
 **********************************************************************/
int dataDigit1[8] = {0};
int dataDigit2[8] = {0};
int dataDigit3[8] = {0};
int dataDigit4[8] = {0};
int dataDigit5[8] = {0};
int dataDigit6[8] = {0};
int dataDigit7[8] = {0};
int dataDigit8[8] = {0};

int countDigit1 = 0;
int countDigit2 = 0;
int countDigit3 = 0;
int countDigit4 = 0;
int countDigit5 = 0;
int countDigit6 = 0;
int countDigit7 = 0;
int countDigit8 = 0;

int valueDigit1 = 0;
int valueDigit2 = 0;
int valueDigit3 = 0;
int valueDigit4 = 0;
int valueDigit5 = 0;
int valueDigit6 = 0;
int valueDigit7 = 0;
int valueDigit8 = 0;

bool firstStrobe = true;


/************************************************
 * Data Processing
 ***********************************************/
int dataToValue(int rawDigitData[8]) {
  
  //pc.printf("The data is: %d%d%d%d%d%d%d%d\n", rawDigitData[0], rawDigitData[1], rawDigitData[2], rawDigitData[3],
  //                                        rawDigitData[4], rawDigitData[5], rawDigitData[6], rawDigitData[7]);

  if( (rawDigitData[0] == 0) && (rawDigitData[1] == 0) && (rawDigitData[2] == 1) && (rawDigitData[3] == 1) && 
      (rawDigitData[4] == 0) && (rawDigitData[5] == 0) && (rawDigitData[6] == 0) && (rawDigitData[7] == 0) ) {
        return 1;
  }
  else if( (rawDigitData[0] == 0) && (rawDigitData[1] == 1) && (rawDigitData[2] == 1) && (rawDigitData[3] == 0) && 
           (rawDigitData[4] == 1) && (rawDigitData[5] == 1) && (rawDigitData[6] == 1) && (rawDigitData[7] == 0) ) {
        return 2;
  }
  else if( (rawDigitData[0] == 0) && (rawDigitData[1] == 1) && (rawDigitData[2] == 1) && (rawDigitData[3] == 1) && 
           (rawDigitData[4] == 1) && (rawDigitData[5] == 0) && (rawDigitData[6] == 1) && (rawDigitData[7] == 0) ) {
        return 3;
  }
  else if( (rawDigitData[0] == 1) && (rawDigitData[1] == 0) && (rawDigitData[2] == 1) && (rawDigitData[3] == 1) && 
           (rawDigitData[4] == 1) && (rawDigitData[5] == 0) && (rawDigitData[6] == 0) && (rawDigitData[7] == 0) ) {
        return 4;
  }
  else if( (rawDigitData[0] == 1) && (rawDigitData[1] == 1) && (rawDigitData[2] == 0) && (rawDigitData[3] == 1) && 
           (rawDigitData[4] == 1) && (rawDigitData[5] == 0) && (rawDigitData[6] == 1) && (rawDigitData[7] == 0) ) {
        return 5;
  }
  else if( (rawDigitData[0] == 1) && (rawDigitData[1] == 1) && (rawDigitData[2] == 0) && (rawDigitData[3] == 1) && 
           (rawDigitData[4] == 1) && (rawDigitData[5] == 1) && (rawDigitData[6] == 1) && (rawDigitData[7] == 0) ) {
        return 6;
  }
  else if( (rawDigitData[0] == 0) && (rawDigitData[1] == 1) && (rawDigitData[2] == 1) && (rawDigitData[3] == 1) && 
           (rawDigitData[4] == 0) && (rawDigitData[5] == 0) && (rawDigitData[6] == 0) && (rawDigitData[7] == 0) ) {
        return 7;
  }
  else if( (rawDigitData[0] == 1) && (rawDigitData[1] == 1) && (rawDigitData[2] == 1) && (rawDigitData[3] == 1) && 
           (rawDigitData[4] == 1) && (rawDigitData[5] == 1) && (rawDigitData[6] == 1) && (rawDigitData[7] == 0) ) {
        return 8;
  }
  else if( (rawDigitData[0] == 1) && (rawDigitData[1] == 1) && (rawDigitData[2] == 1) && (rawDigitData[3] == 1) && 
           (rawDigitData[4] == 1) && (rawDigitData[5] == 0) && (rawDigitData[6] == 1) && (rawDigitData[7] == 0) ) {
        return 9;
  }
  else if( (rawDigitData[0] == 1) && (rawDigitData[1] == 1) && (rawDigitData[2] == 1) && (rawDigitData[3] == 1) && 
           (rawDigitData[4] == 0) && (rawDigitData[5] == 1) && (rawDigitData[6] == 1) && (rawDigitData[7] == 0) ) {
        return 0;
  }
  else {
    return -1;
  }
}

void dataProccesing() {
  if(countDigit1 == 8) {
    valueDigit1 = dataToValue(dataDigit1);
  }
  if(countDigit2 == 8) {
    valueDigit2 = dataToValue(dataDigit2);
  }
  if(countDigit3 == 8) {
    valueDigit3 = dataToValue(dataDigit3);
  }
  if(countDigit4 == 8) {
    valueDigit4 = dataToValue(dataDigit4);
  }
  if(countDigit5 == 8) {
    valueDigit5 = dataToValue(dataDigit5);
  }
  if(countDigit6 == 8) {
    valueDigit6 = dataToValue(dataDigit6);
  }
  if(countDigit7 == 8) {
    valueDigit7 = dataToValue(dataDigit7);
  }
  if(countDigit8 == 8) {
    valueDigit8 = dataToValue(dataDigit8);
  }

  pc.printf("%d.%d.%d.%d.%d.%d.%d.%d\n",  valueDigit1, valueDigit2, valueDigit3, valueDigit4,
                                        valueDigit5, valueDigit6, valueDigit7, valueDigit8);

  
}


/************************************************
 * INTERRUPT SERVICE ROUTINE
 ***********************************************/
void strobeInput() {
  if(firstStrobe) {
    firstStrobe = false;
  }
  else {
    __disable_irq();  // Disable Interrupts
    dataProccesing();
    firstStrobe = true;
    __enable_irq();
  }

  countDigit1 = 0;
  countDigit2 = 0;
  countDigit3 = 0;
  countDigit4 = 0;
  countDigit5 = 0;
  countDigit6 = 0;
  countDigit7 = 0;
  countDigit8 = 0;
}

void newDataDigit1() {
  dataDigit1[countDigit1] = data.read();
  countDigit1++;
}

void newDataDigit2() {
  dataDigit2[countDigit2] = data.read();
  countDigit2++;
}

void newDataDigit3() {
  dataDigit3[countDigit3] = data.read();
  countDigit3++;
}

void newDataDigit4() {
  dataDigit4[countDigit4] = data.read();
  countDigit4++;
}

void newDataDigit5() {
  dataDigit5[countDigit5] = data.read();
  countDigit5++;
}

void newDataDigit6() {
  dataDigit6[countDigit6] = data.read();
  countDigit6++;
}

void newDataDigit7() {
  dataDigit7[countDigit7] = data.read();
  countDigit7++;
}

void newDataDigit8() {
  dataDigit8[countDigit8] = data.read();
  countDigit8++;
}

/************************************************
 * MAIN
 ***********************************************/
int main() {
  led.write(1);

  strobe.rise(&strobeInput);

  digit1.rise(&newDataDigit1);
  digit2.rise(&newDataDigit2);
  digit3.rise(&newDataDigit3);
  digit4.rise(&newDataDigit4);
  digit5.rise(&newDataDigit5);
  digit6.rise(&newDataDigit6);
  digit7.rise(&newDataDigit7);
  digit8.rise(&newDataDigit8);

  // put your setup code here, to run once:

  while(1) {
    // put your main code here, to run repeatedly:
  }
}