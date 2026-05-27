#include <gtest/gtest.h>

#include "commands/PauseCommand.h"

TEST(PauseCommandTest, ReturnsDoneAndAcceptsPayload)
{
    PauseCommand command;

    command.prepare();
    EXPECT_EQ(command.run(), CommandState::Done);

    uint8_t payload[2] = {0xAA, 0x55};
    EXPECT_TRUE(command.setPayload(payload, sizeof(payload)));
}
