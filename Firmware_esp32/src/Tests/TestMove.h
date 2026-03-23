#ifndef TESTMOVE_H
#define TESTMOVE_H

#include "../Controller.h"

class TestMove
{
public:
    TestMove();
    bool run();
private:
    Controller* testCtrl;
};

#endif