#ifndef MOSFET_H
#define MOSFET_H

class Mosfet
{
public:
    Mosfet(int pin);
    ~Mosfet();
    void on();
    void off();
    bool getState();
private:
    int pin;    
    bool state;
};

#endif