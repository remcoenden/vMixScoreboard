/***************************************
 * Test program for the vMixScoreboard
 * Application on the microcontroller
 * Written for Raspberry Pi 4B
 * 
 * Author: 	Remco van den Enden
 * Date: 	26 August 2020
 **************************************/

/***************************************
 * INCLUDES
 **************************************/
#include <wiringPi.h>
#include "stdio.h"
#include "stdbool.h"


/***************************************
 * WIRINGPI SETUP
 **************************************/
 #define dataPin 	0	// Physical Pin 11 as data output
 #define strobePin 	1	// Physical Pin 12 as strobe output
 #define clockD1Pin 2	// Physical Pin 13 as clock digit 1
 #define clockD2Pin 3	// Physical Pin 15 as clock digit 2
 #define clockD3Pin 4	// Physical Pin 16 as clock digit 3
 #define clockD4Pin 5	// Physical Pin 18 as clock digit 4
 #define clockD5Pin 6	// Physical Pin 22 as clock digit 5
 #define clockD6Pin 7	// Physical Pin  7 as clock digit 6
 #define clockD7Pin 8	// Physical Pin  3 as clock digit 7
 #define clockD8Pin 9	// Physical Pin  5 as clock digit 8	
 
 
 void setupWiringPi() {
	 wiringPiSetup();
	 
	 pinMode(dataPin, OUTPUT);		
	 pinMode(strobePin, OUTPUT);	
	 pinMode(clockD1Pin, OUTPUT);	
	 pinMode(clockD2Pin, OUTPUT);	
	 pinMode(clockD3Pin, OUTPUT);	
	 pinMode(clockD4Pin, OUTPUT);	
	 pinMode(clockD5Pin, OUTPUT);	
	 pinMode(clockD6Pin, OUTPUT);	
	 pinMode(clockD7Pin, OUTPUT);	
	 pinMode(clockD8Pin, OUTPUT);	 
 }
 
 
 /***************************************
 * DIGIT DATA SIMULATION
 **************************************/
void pushData(bool value, int clockPin) {
	digitalWrite(clockPin, LOW);
	switch(value) {
		case true:
			digitalWrite(dataPin, HIGH);	// Make data pin high
			digitalWrite(clockPin, HIGH);	// High pulse on the clock
			delayMicroseconds(2);			// Wait
			digitalWrite(clockPin, LOW);	// Make clock low
			delayMicroseconds(2);			// Wait
			break;
		case false:
			digitalWrite(dataPin, LOW);		// Make data pin low
			digitalWrite(clockPin, HIGH);	// High pulse on the clock
			delayMicroseconds(2);			// Wait
			digitalWrite(clockPin, LOW);	// Make clock low
			delayMicroseconds(2);			// Wait
	}
}

void pushStrobe(void) {
	digitalWrite(strobePin, HIGH);
	delayMicroseconds(5);
	digitalWrite(strobePin, LOW);
	delayMicroseconds(5);
}

void pushNumber(int value, int clockPin) {
	// Check is value is in range
	if( (value < -1) || (value > 9) ) {
		printf("Value is out of range!\r\n");
		return;
	}
	
	const int dataValue0[8] = {1, 1, 1, 1, 0, 1, 1, 0};
	const int dataValue1[8] = {0, 0, 1, 1, 0, 0, 0, 0};
	const int dataValue2[8] = {0, 1, 1, 0, 1, 1, 1, 0};
	const int dataValue3[8] = {0, 1, 1, 1, 1, 0, 1, 0};
	const int dataValue4[8] = {1, 0, 1, 1, 1, 0, 0, 0};
	const int dataValue5[8] = {1, 1, 0, 1, 1, 0, 1, 0};
	const int dataValue6[8] = {1, 1, 0, 1, 1, 1, 1, 0};
	const int dataValue7[8] = {0, 1, 1, 1, 0, 0, 0, 0};
	const int dataValue8[8] = {1, 1, 1, 1, 1, 1, 1, 0};
	const int dataValue9[8] = {1, 1, 1, 1, 1, 0, 1, 0};
	const int dataValueNaN[8] = {0, 0, 0, 0, 0, 0, 0, 0};
	
	switch(value) {
		case 0:
			for(int i = 0; i < 8; i++) {
				pushData(dataValue0[i], clockPin);
			}
			break;
		case 1:
			for(int i = 0; i < 8; i++) {
				pushData(dataValue1[i], clockPin);
			}
			break;
		case 2:
			for(int i = 0; i < 8; i++) {
				pushData(dataValue2[i], clockPin);
			}
			break;
		case 3:
			for(int i = 0; i < 8; i++) {
				pushData(dataValue3[i], clockPin);
			}
			break;
		case 4:
			for(int i = 0; i < 8; i++) {
				pushData(dataValue4[i], clockPin);
			}
			break;
		case 5:
			for(int i = 0; i < 8; i++) {
				pushData(dataValue5[i], clockPin);
			}
			break;
		case 6:
			for(int i = 0; i < 8; i++) {
				pushData(dataValue6[i], clockPin);
			}
			break;
		case 7:
			for(int i = 0; i < 8; i++) {
				pushData(dataValue7[i], clockPin);
			}
			break;
		case 8:
			for(int i = 0; i < 8; i++) {
				pushData(dataValue8[i], clockPin);
			}
			break;
		case 9:
			for(int i = 0; i < 8; i++) {
				pushData(dataValue9[i], clockPin);
			}
			break;
		case -1:
			for(int i = 0; i < 8; i++) {
				pushData(dataValueNaN[i], clockPin);
			}
			break;
	}
}


/***************************************
 * MAIN
 **************************************/
int main(void) {
	printf("Start the program!\r\n");
	setupWiringPi();
	
	for(int i = 0; i < 2; i++) {
		pushNumber(1, clockD1Pin);
		pushNumber(-1, clockD2Pin);
		pushNumber(3, clockD3Pin);
		pushNumber(4, clockD4Pin);
		pushNumber(5, clockD5Pin);
		pushNumber(6, clockD6Pin);
		pushNumber(7, clockD7Pin);
		pushNumber(8, clockD8Pin);
		pushStrobe();
		delay(1);
	}
	
	return 0;
}
