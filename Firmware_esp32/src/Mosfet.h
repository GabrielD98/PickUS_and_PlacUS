#ifndef MOSFET_H
#define MOSFET_H

#include <stdint.h>

class Mosfet
{
public:
    Mosfet(uint8_t pin);
    ~Mosfet();
    void on();
    void off();
    bool getState() const;
private:
    uint8_t pin;
    bool state;
};

#endif