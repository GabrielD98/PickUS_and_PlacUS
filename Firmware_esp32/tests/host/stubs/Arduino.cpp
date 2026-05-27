#include "Arduino.h"

Stream Serial;

static uint64_t gMillis = 0;

uint64_t millis()
{
    return gMillis;
}

void setMillis(uint64_t value)
{
    gMillis = value;
}
