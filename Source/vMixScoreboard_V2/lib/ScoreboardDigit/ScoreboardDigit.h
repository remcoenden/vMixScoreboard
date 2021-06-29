/************************************************
 * vMixScoreboard V2
 *
 * Created by: Remco van den Enden
 * Last edited by: Remco van den Enden
 * Last edited on: Tue Jun 29 2021
************************************************/

/* Used for figuring out how to create scalable interrupts */
/* https://forum.arduino.cc/t/a-class-and-an-interrupt-defined-within-it/352213 */

#ifndef SCOREBOARD_DIGIT
#define SCOREBOARD_DIGIT


/**********************************************************************
 * INCLUDES
 **********************************************************************/
#include <Arduino.h>
#include <array>


/**********************************************************************
 * CLASS DEFINITIONS
 **********************************************************************/
class ScoreboardDigit {
public:
    /* Constructor(s) */
    ScoreboardDigit(uint8_t digitData, uint8_t digitClock);

    /* Destructor */
    ~ScoreboardDigit();

    /* Methods */
    void setupInterruptHandler(uint8_t pin, void (*ISR)(void), int value);
    void newDataCallback();

    int8_t getValue();

    /* Variables */

private:
    /* Ardiono hardware dirvers (digital IO for example) */
    uint8_t  _digitData;
    uint8_t  _digitClock;

    /* Methods */
    void dataToValue();
    void resetDataBuffer();

    /* Variables */
    std::array<uint8_t, 8>  _readData   { {'\0'} }; // Used to store the data received from the scoreboard
    uint8_t                 _dataCount  {0};    // Used to keep track of bits received from the scoreboard
    int8_t                  _digitValue {0};

    /* Constants */
    /* These arrays are used to compare the receive data to a real value */
    std::array<uint8_t, 8> digitValue_1 { {0, 0, 1, 1, 0, 0, 0, 0} };
    std::array<uint8_t, 8> digitValue_2 { {0, 1, 1, 0, 1, 1, 1, 0} };
    std::array<uint8_t, 8> digitValue_3 { {0, 1, 1, 1, 1, 0, 1, 0} };
    std::array<uint8_t, 8> digitValue_4 { {1, 0, 1, 1, 1, 0, 0, 0} };
    std::array<uint8_t, 8> digitValue_5 { {1, 1, 0, 1, 1, 0, 1, 0} };
    std::array<uint8_t, 8> digitValue_6 { {1, 1, 0, 1, 1, 1, 1, 0} };
    std::array<uint8_t, 8> digitValue_7 { {0, 1, 1, 1, 0, 0, 0, 0} };
    std::array<uint8_t, 8> digitValue_8 { {1, 1, 1, 1, 1, 1, 1, 0} };
    std::array<uint8_t, 8> digitValue_9 { {1, 1, 1, 1, 1, 0, 1, 0} };
    std::array<uint8_t, 8> digitValue_0 { {1, 1, 1, 1, 0, 1, 1, 0} };
    
protected:
    /* Methods */

    /* Variables */

};

#endif /* SCOREBOARD_DIGIT */
