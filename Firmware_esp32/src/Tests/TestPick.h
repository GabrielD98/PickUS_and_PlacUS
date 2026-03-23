#ifndef TESTPICK_H
#define TESTPICK_H

#include "../Controller.h"

class TestPick
{
public:
    TestPick();
    bool run();
private:
    Controller* testCtrl;
};

#endif