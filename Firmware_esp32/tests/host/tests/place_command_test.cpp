#include <gtest/gtest.h>

#include "commands/PlaceCommand.h"
#include "hardware/mosfet.h"
#include "hardware/pressureSensor.h"

TEST(PlaceCommandTest, OpensValveAndStopsPumpWhenDone)
{
    Mosfet valve(1);
    Mosfet pump(2);
    PressureSensor sensor(3, 4);

    PlacingHardware hardware{{&valve}, &pump, {&sensor}};
    PlaceCommand command(&hardware);

    PlacingPayload payload{0, 50};
    ASSERT_TRUE(command.setPayload(reinterpret_cast<uint8_t*>(&payload), sizeof(payload)));

    pump.on();
    command.prepare();
    EXPECT_TRUE(valve.getState());

    sensor.setPressureKPa(40.0f);
    EXPECT_EQ(command.run(), CommandState::InProgress);

    sensor.setPressureKPa(60.0f);
    EXPECT_EQ(command.run(), CommandState::Done);
    EXPECT_FALSE(pump.getState());
}
