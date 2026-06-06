#include "limitswitch.h"

LimitSwitch::LimitSwitch(uint8_t pin, bool activeLOW)
{
    this->pin = pin;
    this->activeLOW = activeLOW;

    // Switch type selection
    pinMode(pin, activeLOW ? INPUT_PULLUP : INPUT_PULLDOWN);
}


bool LimitSwitch::isTriggered() const
{
    bool pinRead = digitalRead(this->pin);
    return activeLOW ? !pinRead : pinRead;
}
