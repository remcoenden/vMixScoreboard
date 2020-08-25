#include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/types.h>
#include <unistd.h>

#define DATA_PIN_NUMBER 7
#define STROBE_PIN_NUMBER 21
#define CLOCK_DIGIT1_PIN_NUMBER 22

void *printDigitThread();
pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;

int getDigit = 0;

int Digit1Data[8] = {0};
int Digit1Count = 0;

void strobeInterrupt(void) {
	if(Digit1Count >= 7) {
		getDigit = 1;
	}
	Digit1Count = 0;
}

void clockD1Interrupt(void) {
	Digit1Data[Digit1Count] = digitalRead(DATA_PIN_NUMBER);
	Digit1Count++;
}

void setupGPIO(void) {
	// Init wiringPi
	wiringPiSetup();
	
	// Setup data signal
	pinMode(DATA_PIN_NUMBER, INPUT);
	
	// Setup strobe signal
	wiringPiISR(STROBE_PIN_NUMBER, INT_EDGE_RISING, &strobeInterrupt); 
	
	// Setup clock signals
	wiringPiISR(CLOCK_DIGIT1_PIN_NUMBER, INT_EDGE_RISING, clockD1Interrupt);
}

int main (void) {
	printf("Starting up the program\n");
	setupGPIO();
	
	int threadReturn;
	pthread_t thread1;
	
	if((threadReturn = pthread_create(&thread1, NULL, &printDigitThread, NULL))) {
		printf("Thread creating failed %d\n", threadReturn);
	}
	
	pthread_join(thread1, NULL);
		
	return 0 ;
}

void *printDigitThread() {
	while(1) {
		if(getDigit == 1) {
			printf("%d%d%d%d%d%d%d%d\n", Digit1Data[0], Digit1Data[1], Digit1Data[2],
										 Digit1Data[3], Digit1Data[4], Digit1Data[5],
										 Digit1Data[6], Digit1Data[7]);
		}
		usleep(5);
	}
}
