/**
 * @file testcom.h
 * @author PickusAndPlacus
 * @brief 
 * @version
 * @date
 */

#ifndef TESTCOM_H
#define TESTCOM_H

#include "../Controller.h"

class TestCom
{
public:
    TestCom(Controller* ctrl);
    bool run(uint32_t durationMs);

private:
    Controller* ctrl;
};

#endif