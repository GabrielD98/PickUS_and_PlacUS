#include <gtest/gtest.h>

#include "commands/HomeCommand.h"

TEST(HomeCommandTest, AcceptsPayloadAndReturnsDone)
{
    AccelStepper motorX;
    AccelStepper motorY;
    AccelStepper motorZ;
    AccelStepper motorYaw;
    LimitSwitch switchX(1);
    LimitSwitch switchY(2);
    LimitSwitch switchZ(3);

    HomingHardware hardware{&motorX, &motorY, &motorZ, &motorYaw, &switchX, &switchY, &switchZ};
    HomeCommand command(&hardware);

    HomingPayload payload{{1, 2, 3, 4}};
    EXPECT_TRUE(command.setPayload(reinterpret_cast<uint8_t*>(&payload), sizeof(payload)));

    command.prepare();

    EXPECT_EQ(command.run(), CommandState::InProgress);

    switchZ.setTriggered(true);
    EXPECT_EQ(command.run(), CommandState::InProgress);

    EXPECT_EQ(command.run(), CommandState::InProgress);

    switchX.setTriggered(true);
    EXPECT_EQ(command.run(), CommandState::InProgress);

    EXPECT_EQ(command.run(), CommandState::InProgress);

    switchY.setTriggered(true);
    EXPECT_EQ(command.run(), CommandState::InProgress);

    EXPECT_EQ(command.run(), CommandState::InProgress);
    EXPECT_EQ(command.run(), CommandState::Done);
}
