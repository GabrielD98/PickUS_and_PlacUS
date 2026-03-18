#ifndef LIMITSWITCH_H
#define LIMITSWITCH_H

#include <Arduino.h>

class LimitSwitch
{
public:
    LimitSwitch(uint8_t pin, bool activeLOW = true);

    /** Returns true when the switch is triggered. */
    bool isTriggered() const;

private:
    uint8_t _pin;
    bool    _activeLOW;
};

#endif // LIMITSWITCH_H
