#include <gtest/gtest.h>

#include "commands/PickCommand.h"
#include "hardware/mosfet.h"
#include "hardware/pressureSensor.h"

TEST(PickCommandTest, PreparesHardwareAndCompletesOnPressure)
{
    Mosfet valve(1);
    Mosfet pump(2);
    PressureSensor sensor(3, 4);

    PickingHardware hardware{{&valve}, &pump, {&sensor}};
    PickCommand command(&hardware);

    PickingPayload payload{0, 50};
    ASSERT_TRUE(command.setPayload(reinterpret_cast<uint8_t*>(&payload), sizeof(payload)));

    valve.on();
    pump.off();
    command.prepare();
    EXPECT_TRUE(pump.getState());
    EXPECT_FALSE(valve.getState());

    sensor.setPressureKPa(60.0f);
    EXPECT_EQ(command.run(), CommandState::InProgress);

    sensor.setPressureKPa(40.0f);
    EXPECT_EQ(command.run(), CommandState::Done);
}
