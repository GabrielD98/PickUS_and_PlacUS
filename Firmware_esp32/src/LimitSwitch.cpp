#include "LimitSwitch.h"

LimitSwitch::LimitSwitch(uint8_t pin, bool activeLOW)
    : _pin(pin), _activeLOW(activeLOW)
{
    pinMode(_pin, _activeLOW ? INPUT_PULLUP : INPUT_PULLDOWN);
}

bool LimitSwitch::isTriggered() const
{
    bool pin = digitalRead(_pin);
    return _activeLOW ? !pin : pin;
}
