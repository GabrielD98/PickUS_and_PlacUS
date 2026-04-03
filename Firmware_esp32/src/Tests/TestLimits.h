#ifndef TESTLIMITS_H
#define TESTLIMITS_H

#include "../Controller.h"

/**
 * @brief Confirms the proper replacement of targeted locations exceeding imposed boundaries.
 */
class TestLimits
{
public:
    TestLimits();

    /**
     * @brief Verify if a location exceeding boundaries in all degree of freedom accessible is brought back to the closest boundaries.
     * 
     * @return true if passed, else false
     */
    bool run();
};

#endif