/**
 * @file testlimits.h
 * @author PickusAndPlacus
 * @brief Class to execute a test of hardcoded movement restrictions.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef TESTLIMITS_H
#define TESTLIMITS_H

#include "../controller.h"

/**
 * @brief Confirms the proper replacement of targeted locations exceeding imposed boundaries.
 */
class TestLimits
{
public:
    TestLimits();

    /**
     * @brief Verify if a location exceeding boundaries in all degree of freedom accessible
     * is brought back to the closest boundaries.
     * @return true if passed, else false
     */
    bool run();
};

#endif