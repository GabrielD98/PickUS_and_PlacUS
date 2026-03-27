#ifndef TESTHOME_H
#define TESTHOME_H

#include "../Controller.h"

class TestHome
{
public:
    TestHome();
    bool run();
private:
    Controller* testCtrl;
};

#endif