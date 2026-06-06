#include <gtest/gtest.h>

#include "commands/PumpCommand.h"
#include "hardware/mosfet.h"

TEST(PumpCommandTest, TogglesPumpBasedOnPayload)
{
    Mosfet pump(1);
    PumpHardware hardware{&pump};
    PumpCommand command(&hardware);

    PumpPayload payload{1};
    ASSERT_TRUE(command.setPayload(reinterpret_cast<uint8_t*>(&payload), sizeof(payload)));
    command.prepare();
    EXPECT_TRUE(pump.getState());

    payload.enabled = 0;
    ASSERT_TRUE(command.setPayload(reinterpret_cast<uint8_t*>(&payload), sizeof(payload)));
    command.prepare();
    EXPECT_FALSE(pump.getState());

    EXPECT_EQ(command.run(), CommandState::Done);
}

TEST(PumpCommandTest, HandlesNullHardware)
{
    PumpCommand command(nullptr);

    PumpPayload payload{1};
    EXPECT_TRUE(command.setPayload(reinterpret_cast<uint8_t*>(&payload), sizeof(payload)));
    command.prepare();
    EXPECT_EQ(command.run(), CommandState::Done);
}
