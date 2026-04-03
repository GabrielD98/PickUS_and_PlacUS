/**
 * @file mosfet.h
 * @author PickusAndPlacus
 * @brief Class to control a mosfet as an electrical switch for a physical component.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef MOSFET_H
#define MOSFET_H

#include <stdint.h>

/**
 * @brief Serves as an electrical switch for a physical component.
 * Store an associated digital pin's identifier and the switch's state.
 */
class Mosfet
{
public:
    /**
     * @brief Associate the mosfet to an electrical source pin of a physical system.
     * @param pin Electrical source pin connected to a physical system.
     */
    Mosfet(uint8_t pin);
    
    /**
     * @brief Deactivate electrical output when the object is destroyed.
     */
    ~Mosfet();

    /**
     * @brief Activate electrical output.
     */
    void on();

    /**
     * @brief Deactivate electrical output.
     */
    void off();

    /**
     * @brief Give the current mosfet state.
     * 
     * @return True if the pin output is active, else false.
     */
    bool getState();

private:
    /**
     * @brief Associated digital pin identifier.
     */
    uint8_t pin;

    /**
     * @brief Mosfet's state. True if the pin is at HIGH, else false.
     */
    bool state;
};

#endif // MOSFET_H