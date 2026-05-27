#pragma once

#include <cstdint>

class PressureSensor
{
public:
    PressureSensor(uint8_t clkPin, uint8_t dataPin)
        : clkPin(clkPin), dataPin(dataPin)
    {
    }

    void init()
    {
    }

    void update()
    {
    }

    float getPressureKPa()
    {
        return pressure;
    }

    void setPressureKPa(float value)
    {
        pressure = value;
    }

private:
    uint8_t clkPin{0};
    uint8_t dataPin{0};
    float pressure{0.0f};
};
