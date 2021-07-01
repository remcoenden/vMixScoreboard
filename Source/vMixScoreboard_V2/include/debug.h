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

#include <stdarg.h>

/***********************************************
 * SETUP
 ***********************************************/
#define SERIAL_DEBUG_OUTPUT true

void initiateSerialDebug() {
    Serial.begin(9600);
}

/***********************************************
 * CONTROL
 ***********************************************/
void printToMonitor(const char* debugGroup_, const char* str_, size_t size_, ...) {
    /* Retreive all the extra arugments
     * https://stackoverflow.com/a/4339447/10546380
     */
    va_list args;
    va_start(args, size_);

    char _buffer[size_ + 10] = {'\0'};

    sprintf( _buffer, "[%-4s] %s\n", debugGroup_, str_ );
    vprintf( _buffer, args );

    va_end(args);
}

/************************************************
 * BASIC DEBUG OUTPUT
 ***********************************************/
/* Set to true for debug output, false for no debug output */
#define USE_DEBUG_BASIC true

/* Create debug messages like: DEBUG("Some debug output"); */
#if USE_DEBUG_BASIC
#define DEBUG(str_, ...) \
    printToMonitor("DBG", (str_), sizeof(str_) / sizeof(str_[0]), ##__VA_ARGS__);
#endif


/************************************************
 * ERROR DEBUG OUTPUT
 ***********************************************/
#define USE_DEBUG_ERROR true

/* Create debug messages like: DEBUG_ERROR("Some debug output"); */
#if USE_DEBUG_ERROR
#define DEBUG_ERROR(str_, ...) \
    printToMonitor("ERR", (str_), sizeof(str_) / sizeof(str_[0]), ##__VA_ARGS__);
#endif


/************************************************
 * WARNING DEBUG OUTPUT
 ***********************************************/
#define USE_DEBUG_WARNING true

#if USE_DEBUG_WARNING
#define DEBUG_WARNING(str_, ...) \
    printToMonitor("WARN", (str_), sizeof(str_) / sizeof(str_[0]), ##__VA_ARGS__);
#endif

/************************************************
 * INTO DEBUG OUTPUT
 ***********************************************/
#define USE_DEBUG_INFO true

#if USE_DEBUG_INFO
#define DEBUG_INFO(str_, ...) \
    printToMonitor("INFO", (str_), sizeof(str_) / sizeof(str_[0]), ##__VA_ARGS__);
#endif

#endif /* DEBUG_CONTROL */