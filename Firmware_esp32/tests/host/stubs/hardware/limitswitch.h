#pragma once

#include <cstdint>

class LimitSwitch
{
public:
    LimitSwitch(uint8_t pin, bool activeLOW = true)
        : pin(pin), activeLOW(activeLOW)
    {
    }

    bool isTriggered() const
    {
        return triggered;
    }

    void setTriggered(bool value)
    {
        triggered = value;
    }

private:
    uint8_t pin{0};
    bool activeLOW{true};
    bool triggered{false};
};
