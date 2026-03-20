#ifndef TESTMOVE_H
#define TESTMOVE_H

#include "Controller.h"

class TestMove
{
public:
    TestMove();
    bool runTest();
private:
    Controller* ctrl;
};



#endif