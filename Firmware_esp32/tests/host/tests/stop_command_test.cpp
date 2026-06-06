#include <gtest/gtest.h>

#include "commands/StopCommand.h"

namespace
{
bool gResetCalled = false;

void resetCallback()
{
    gResetCalled = true;
}
}

TEST(StopCommandTest, InvokesResetCallback)
{
    gResetCalled = false;
    StopCommand command(&resetCallback);

    command.prepare();
    EXPECT_EQ(command.run(), CommandState::Done);
    EXPECT_TRUE(gResetCalled);

    EXPECT_TRUE(command.setPayload(nullptr, 0));
}
