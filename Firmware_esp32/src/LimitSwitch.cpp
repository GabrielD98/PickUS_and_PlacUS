#include "LimitSwitch.h"

LimitSwitch::LimitSwitch(uint8_t pin, bool activeLOW)
{
    this->pin = pin;
    this->activeLOW = activeLOW;

    pinMode(pin, activeLOW ? INPUT_PULLUP : INPUT_PULLDOWN);
}

bool LimitSwitch::isTriggered() const
{
    bool pin = digitalRead(pin);
    return activeLOW ? !pin : pin;
}
