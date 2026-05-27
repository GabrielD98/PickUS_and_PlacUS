#include <gtest/gtest.h>

#include "commands/ValveCommand.h"
#include "hardware/mosfet.h"

TEST(ValveCommandTest, AppliesValveState)
{
    Mosfet valve(1);
    ValveHardware hardware{{&valve}};
    ValveCommand command(&hardware);

    ValvePayload payload{0, 1};
    ASSERT_TRUE(command.setPayload(reinterpret_cast<uint8_t*>(&payload), sizeof(payload)));
    command.prepare();
    EXPECT_TRUE(valve.getState());

    payload.enabled = 0;
    ASSERT_TRUE(command.setPayload(reinterpret_cast<uint8_t*>(&payload), sizeof(payload)));
    command.prepare();
    EXPECT_FALSE(valve.getState());
}

TEST(ValveCommandTest, RejectsInvalidToolhead)
{
    Mosfet valve(1);
    ValveHardware hardware{{&valve}};
    ValveCommand command(&hardware);

    ValvePayload payload{static_cast<uint8_t>(MAX_TOOLHEAD), 1};
    EXPECT_FALSE(command.setPayload(reinterpret_cast<uint8_t*>(&payload), sizeof(payload)));
}
