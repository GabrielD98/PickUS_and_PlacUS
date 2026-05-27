#pragma once

#include <cstdint>

class Mosfet
{
public:
    explicit Mosfet(uint8_t pin)
        : pin(pin)
    {
    }

    void on()
    {
        state = true;
    }

    void off()
    {
        state = false;
    }

    bool getState()
    {
        return state;
    }

    void setState(bool value)
    {
        state = value;
    }

private:
    uint8_t pin{0};
    bool state{false};
};
