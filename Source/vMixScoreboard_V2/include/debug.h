/************************************************
 * vMixScoreboard V2
 *
 * Created by: Remco van den Enden
 * Last edited by: Remco van den Enden
 * Last edited on: Tue Jun 29 2021
************************************************/

/* Macros for easy serial debugging */
/* https://forum.arduino.cc/t/debug-version-of-serial-print/560360/3 */

#ifndef DEBUG_CONTROL
#define DEBUG_CONTROL

/***********************************************
 * INCLUDES
 ***********************************************/
#include <Arduino.h>

/***********************************************
 * SETUP
 ***********************************************/
#define SERIAL_DEBUG_OUTPUT true

void initiateSerialDebug() {
    Serial.begin(9600);
}

/************************************************
 * BASIC DEBUG OUTPUT
 ***********************************************/
/* Set to true for debug output, false for no debug output */
#define DEBUG_BASIC true

/* Create debug messages like: DEBUG_SERIAL.println("Some debug output"); */
#define DEBUG_BASIC_SERIAL \
    if (DEBUG_BASIC) Serial

void DEBUG(const char* str) {
    DEBUG_BASIC_SERIAL.println((String)"[DBG ] " + str);
}


/************************************************
 * ERROR DEBUG OUTPUT
 ***********************************************/
#define DEBUG_ERROR true

#define DEBUG_ERROR_SERIAL \
    if (DEBUG_ERROR) Serial

void DEBUG_ERR(const char* str) {
    DEBUG_ERROR_SERIAL.println((String)"[ERR ] " + str);
}


/************************************************
 * WARNING DEBUG OUTPUT
 ***********************************************/
#define DEBUG_WARNING true

#define DEBUG_WARNING_SERIAL \
    if (DEBUG_WARNING) Serial

void DEBUG_WARN(const char* str) {
    DEBUG_ERROR_SERIAL.println((String)"[WARN] " + str);
}

/************************************************
 * INTO DEBUG OUTPUT
 ***********************************************/
#define DEBUG_INFO true

#define DEBUG_INFO_SERIAL \
    if (DEBUG_INFO) Serial

void DEBUG_INF(const char* str) {
    DEBUG_ERROR_SERIAL.println((String)"[INFO] " + str);
}

#endif /* DEBUG_CONTROL */