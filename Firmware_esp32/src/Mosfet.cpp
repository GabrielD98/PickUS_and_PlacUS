#include "Mosfet.h"
#include <Arduino.h>

Mosfet::Mosfet(int pin)
{
    this->pin = pin;
    this->state = false;
    pinMode(this->pin, OUTPUT);
}

Mosfet::~Mosfet()
{
    this->off();
}

void Mosfet::on()
{
    digitalWrite(this->pin, HIGH);
    this->state = true;
}

void Mosfet::off()
{
    digitalWrite(this->pin, LOW);
    this->state = false;
}

bool Mosfet::getState()
{
    return this->state;
}