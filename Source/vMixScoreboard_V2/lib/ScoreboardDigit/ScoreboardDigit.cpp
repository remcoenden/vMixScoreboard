/************************************************
 * vMixScoreboard V2
 *
 * Created by: Remco van den Enden
 * Last edited by: Remco van den Enden
 * Last edited on: Tue Jun 29 2021
************************************************/


/**********************************************************************
 * INCLUDES
 **********************************************************************/
#include "ScoreboardDigit.h"

/**********************************************************************
 * CONSTRUCTOR / DESTRUCTOR
 **********************************************************************/
ScoreboardDigit::ScoreboardDigit(uint8_t digitData, uint8_t digitClock) :
                                _digitData(digitData),
                                _digitClock(digitClock) {
    /* Initiate the data and clock signal to input and interrupt inputs */
    pinMode(_digitData, INPUT);
    pinMode(_digitClock, INPUT);
}

ScoreboardDigit::~ScoreboardDigit() {
    //TODO Write proper destructor
}


/**********************************************************************
 * PUBLIC METHODS
 **********************************************************************/
void ScoreboardDigit::setupInterruptHandler(uint8_t pin, void (*ISR)(void), int value) {
    attachInterrupt(digitalPinToInterrupt(pin), ISR, value);
}

void ScoreboardDigit::newDataCallback() {
    if (_dataCount < 7) {
        _readData[_dataCount] = digitalRead(_digitData);
        _dataCount++;
    }
    else {
        // Error
    }
}

int8_t ScoreboardDigit::getValue() {
    dataToValue();
    resetDataBuffer();
    return _digitValue;
}

/**********************************************************************
 * PRIVATE METHODS
 **********************************************************************/
void ScoreboardDigit::dataToValue() {
    /* Make sure there are eight valid digits stored in the array to prevent exceptions */
    if (_dataCount != 7)
        return;
    
    /* Check the read array against the presents to determine the digit value */
    if (_readData == digitValue_1)
        _digitValue =  1;
    else if (_readData == digitValue_2)
        _digitValue =  2;
    else if (_readData == digitValue_3)
        _digitValue =  3;
    else if (_readData == digitValue_4)
        _digitValue =  4;
    else if (_readData == digitValue_5)
        _digitValue =  5;
    else if (_readData == digitValue_6)
        _digitValue =  6;
    else if (_readData == digitValue_7)
        _digitValue =  7;
    else if (_readData == digitValue_8)
        _digitValue =  8;
    else if(_readData == digitValue_9)
        _digitValue =  9;
    else if (_readData == digitValue_0)
        _digitValue =  0;
    return;
}

void ScoreboardDigit::resetDataBuffer() {
    /* Fill the read buffer with '\0' to make sure all previous data is ereased */
    std::fill(_readData.begin(), _readData.end(), '\0');
    /* Start filling the buffer from zero */
    _dataCount = 0;
}