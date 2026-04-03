/**
 * @file testcom.h
 * @author PickusAndPlacus
 * @brief Class to execute a communication test between the UI and the controller.
 * @version 1.0
 * @date 17/04/2026
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