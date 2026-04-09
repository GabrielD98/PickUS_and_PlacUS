/**
 * @file limitSwitch.h
 * @author PickusAndPlacus
 * @brief Class to control a limit switch output interpretation.
 * @version 1.0
 * @date 17/04/2026
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
    * @brief Associate the switch to a type (pullup or pulldown) and the switch's output to a pin.
     * @param pin Digital pin connected to the limit switch's output.
    * @param activeLOW True if the switch is active when the pin reads LOW, false if active when HIGH.
     */
    LimitSwitch(uint8_t pin, bool activeLOW = true);

    /**
    * @brief Returns true when the pin state matches the configured active state.
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
