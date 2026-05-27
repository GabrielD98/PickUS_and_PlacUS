#include <gtest/gtest.h>

#include "CommandHandler.h"
#include "DataHandler.h"

namespace
{
DataHandlerHardware makeHardware(
    AccelStepper* motorX,
    AccelStepper* motorY,
    AccelStepper* motorZ,
    AccelStepper* motorYaw,
    Mosfet* valve,
    Mosfet* pump,
    PressureSensor* sensor)
{
    DataHandlerHardware hardware{};
    hardware.motorX = motorX;
    hardware.motorY = motorY;
    hardware.motorZ = motorZ;
    hardware.motorYaw = motorYaw;
    hardware.valve[0] = valve;
    hardware.pump = pump;
    hardware.pressureSensor[0] = sensor;
    return hardware;
}
}

TEST(DataHandlerTest, UpdatesStateAndHardwareSnapshots)
{
    AccelStepper motorX;
    AccelStepper motorY;
    AccelStepper motorZ;
    AccelStepper motorYaw;
    Mosfet valve(1);
    Mosfet pump(2);
    PressureSensor sensor(3, 4);

    motorX.setCurrentPosition(10);
    motorY.setCurrentPosition(20);
    motorZ.setCurrentPosition(30);
    motorYaw.setCurrentPosition(40);
    valve.on();
    pump.off();
    sensor.setPressureKPa(12.5f);

    CommandHandler handler;
    DataHandlerHardware hardware = makeHardware(&motorX, &motorY, &motorZ, &motorYaw, &valve, &pump, &sensor);
    DataHandler dataHandler(&hardware, &handler);

    dataHandler.updateInfo(MachineState::Running);
    dataModel_t info = dataHandler.getInfo();

    EXPECT_EQ(info.state, MachineState::Running);
    EXPECT_EQ(info.position.x, 10);
    EXPECT_EQ(info.position.y, 20);
    EXPECT_EQ(info.position.z, 30);
    EXPECT_EQ(info.position.yaw, 40);
    EXPECT_FLOAT_EQ(info.pressure[0], 12.5f);
    EXPECT_TRUE(info.valveState[0]);
    EXPECT_FALSE(info.pumpState);
}

TEST(DataHandlerTest, HandlesNullHardware)
{
    CommandHandler handler;
    DataHandler dataHandler(nullptr, &handler);

    dataHandler.updateInfo(MachineState::Ready);
    dataModel_t info = dataHandler.getInfo();

    EXPECT_EQ(info.state, MachineState::Ready);
}
