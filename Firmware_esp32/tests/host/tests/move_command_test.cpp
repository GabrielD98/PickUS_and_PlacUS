#include <gtest/gtest.h>

#include "commands/MoveCommand.h"

TEST(MoveCommandTest, SetsTargetsAndReportsProgress)
{
    MultiStepper system;
    AccelStepper motorX;
    AccelStepper motorY;
    AccelStepper motorZ;
    AccelStepper motorYaw;

    MovingHardware hardware{&system, &motorX, &motorY, &motorZ, &motorYaw};
    MoveCommand command(&hardware);

    MovingPayload payload{{1, 2, 3, 4}, {10, 11, 12, 13}};
    ASSERT_TRUE(command.setPayload(reinterpret_cast<uint8_t*>(&payload), sizeof(payload)));

    command.prepare();
    EXPECT_EQ(motorX.getMaxSpeed(), 10);
    EXPECT_EQ(motorY.getMaxSpeed(), 11);
    EXPECT_EQ(motorZ.getMaxSpeed(), 12);
    EXPECT_EQ(motorYaw.getMaxSpeed(), 13);

    auto targets = system.getTargets();
    EXPECT_EQ(targets[0], 1);
    EXPECT_EQ(targets[1], 2);
    EXPECT_EQ(targets[2], 3);
    EXPECT_EQ(targets[3], 4);

    system.setRunResult(true);
    EXPECT_EQ(command.run(), CommandState::InProgress);

    system.setRunResult(false);
    EXPECT_EQ(command.run(), CommandState::Done);
}
