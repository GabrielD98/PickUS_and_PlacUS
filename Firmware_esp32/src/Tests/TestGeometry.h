/**
 * @file testgeometry.h
 * @author PickusAndPlacus
 * @brief Class to execute a conversion test of movement and associated units.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef TESTGEOMETRY_H
#define TESTGEOMETRY_H

#include "../Controller.h"

/**
 * @brief Confirms that the conversion of locations from mm to step, and then back to mm,
 * returns the initial locations close to a treshold corresponding to a single motor step.
 */
class TestGeometry
{
public:
    TestGeometry();

    /**
     * @brief Converts every coordinates from mm to steps, then converts them back to mm
     * and verify if they are contained inside a treshold.
     * @return true if passed, else false.
     */
    bool run();
};

#endif