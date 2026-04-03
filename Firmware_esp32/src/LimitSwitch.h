/**
 * @file limitSwitch.h
 * @author PickusAndPlacus
 * @brief 
 * @version
 * @date
 */

#ifndef LIMITSWITCH_H
#define LIMITSWITCH_H

#include <Arduino.h>

/**
 * @brief Allows to verify from its output if this specific switch is triggered.
 * Stores the digital pin's identifier associated to the switch's output.
 */
class LimitSwitch
{
public:
    /**
     * @brief Associate the switch to a type (pullup or pulldown) and the switch'soutput to a pin.
     * @param pin Digital pin connected to the limit switch's output.
     * @param activeLOW True for a pullup, false for a  pulldown.
     */
    LimitSwitch(uint8_t pin, bool activeLOW = true);

    /**
     * @brief Returns true for a pullup switch if the pin state is LOW.
     */
    bool isTriggered() const;

private:
    /**
     * @brief Asssociated digital pin identifier.
     */
    uint8_t pin;

    /**
     * @brief True if the switch's activation opens the circuit, else false.
     */
    bool activeLOW;
};

#endif // LIMITSWITCH_H
