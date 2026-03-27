#ifndef TESTPLACE_H
#define TESTPLACE_H

#include "../Controller.h"

class TestPlace
{
public:
    TestPlace();
    bool run();
private:
    Controller* testCtrl;
};

#endif