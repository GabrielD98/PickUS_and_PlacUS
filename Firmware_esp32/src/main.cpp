#include <Arduino.h>
#include <AccelStepper.h>
#include <MultiStepper.h>

#include "../lib/data.hpp"
#include "BoardConfig.h"
#include "CommandHandler.h"
#include "CommunicationHandler.h"
#include "Controller.h"
#include "DataHandler.h"
#include "commands/HomeCommand.h"
#include "commands/MoveCommand.h"
#include "commands/PickCommand.h"
#include "commands/PlaceCommand.h"
#include "commands/PauseCommand.h"
#include "commands/StopCommand.h"
#include "hardware/LimitSwitch.h"
#include "hardware/Mosfet.h"
#include "hardware/PressureSensor.h"
#include "tests/TestRunner.h"

namespace
{
constexpr uint32_t SERIAL_BAUD_RATE = 115200;
constexpr uint32_t SERIAL_STARTUP_DELAY_MS = 3000;
constexpr uint32_t TEST_TASK_STACK = 10000;
constexpr uint32_t COMMUNICATION_TASK_STACK = 10000;
constexpr uint32_t CONTROL_TASK_STACK = 10000;
constexpr uint32_t PRESSURE_TASK_STACK = 4096;
constexpr TickType_t COMMUNICATION_IDLE_DELAY = pdMS_TO_TICKS(10);
constexpr TickType_t TEST_LOOP_DELAY = pdMS_TO_TICKS(100);
constexpr TickType_t PRESSURE_LOOP_DELAY = pdMS_TO_TICKS(50);

static AccelStepper motorX(AccelStepper::DRIVER, PIN_DX_STEP, PIN_DX_DIR);
static AccelStepper motorY(AccelStepper::DRIVER, PIN_DY_STEP, PIN_DY_DIR);
static AccelStepper motorZ(AccelStepper::DRIVER, PIN_DZ_STEP, PIN_DZ_DIR);
static AccelStepper motorYaw(AccelStepper::DRIVER, PIN_DYAW_STEP, PIN_DYAW_DIR);
static MultiStepper motorSystem;

static LimitSwitch limitSwitchX(PIN_LIMSWITCH_X);
static LimitSwitch limitSwitchY(PIN_LIMSWITCH_Y);
static LimitSwitch limitSwitchZ(PIN_LIMSWITCH_Z);

static Mosfet pump(PIN_PUMP);
static Mosfet valve0(PIN_VALVE);
static PressureSensor pressureSensor0(PIN_PSENSOR_CLK, PIN_PSENSOR_DATA);

static CommandHandler commandHandler;

static DataHandlerHardware dataHandlerHw = {
	&motorX,
	&motorY,
	&motorZ,
	&motorYaw,
	{&valve0},
	&pump,
	{&pressureSensor0}
};

static HomingHardware homingHardware = {
	&motorX,
	&motorY,
	&motorZ,
	&motorYaw,
	&limitSwitchX,
	&limitSwitchY,
	&limitSwitchZ
};

static MovingHardware movingHardware = {
	&motorSystem,
	&motorX,
	&motorY,
	&motorZ,
	&motorYaw
};

static PickingHardware pickingHardware = {
	{&valve0},
	&pump,
	{&pressureSensor0}
};

static PlacingHardware placingHardware = {
	{&valve0},
	&pump,
	{&pressureSensor0}
};

static DataHandler dataHandler(&dataHandlerHw, &commandHandler);
static Controller controller(&commandHandler, &dataHandler);
static CommunicationHandler communicationHandler(&Serial);
static TestRunner testRunner(&controller);

static void resetAllCommandsCallback();
static void initializeHardware();
static void registerCommands();
static void communicationLoop(void* pvParameters);
static void controlLoop(void* pvParameters);
static void testLoop(void* pvParameters);
static void pressureUpdateLoop(void* pvParameters);

struct PressureTaskContext
{
	PressureSensor* pressureSensor[MAX_TOOLHEAD];
};

static PressureTaskContext pressureTaskContext = {
	{&pressureSensor0}
};

static void resetAllCommandsCallback()
{
	commandHandler.resetAllCommand();
}

static void initializeHardware()
{
	motorX.setEnablePin(PIN_DX_EN);
	motorY.setEnablePin(PIN_DY_EN);
	motorZ.setEnablePin(PIN_DZ_EN);
	motorYaw.setEnablePin(PIN_DYAW_EN);

	motorX.setPinsInverted(false, false, true);
	motorY.setPinsInverted(false, false, true);
	motorZ.setPinsInverted(false, false, true);
	motorYaw.setPinsInverted(false, false, true);

	motorX.enableOutputs();
	motorY.enableOutputs();
	motorZ.enableOutputs();
	motorYaw.enableOutputs();

	motorSystem.addStepper(motorX);
	motorSystem.addStepper(motorY);
	motorSystem.addStepper(motorZ);
	motorSystem.addStepper(motorYaw);

	pressureSensor0.init();
}

static void registerCommands()
{
	static StopCommand stopCommand(&resetAllCommandsCallback);
	static PauseCommand pauseCommand;
	static MoveCommand moveCommand(&movingHardware);
	static PickCommand pickCommand(&pickingHardware);
	static PlaceCommand placeCommand(&placingHardware);
	static HomeCommand homeCommand(&homingHardware);

	if (!commandHandler.registerCommand(&stopCommand) ||
		!commandHandler.registerCommand(&pauseCommand) ||
		!commandHandler.registerCommand(&moveCommand) ||
		!commandHandler.registerCommand(&pickCommand) ||
		!commandHandler.registerCommand(&placeCommand) ||
		!commandHandler.registerCommand(&homeCommand))
	{
		while (true)
		{
			vTaskDelay(pdMS_TO_TICKS(1000));
		}
	}
}

static void communicationLoop(void* pvParameters)
{
	(void)pvParameters;
	uint8_t payload[MAX_PAYLOAD_SIZE] = {};

	while (true)
	{
		uint16_t payloadSize = 0;
		if (communicationHandler.handleIncoming(payload, payloadSize))
		{
			commandHandler.setCurrentCommand(payload, payloadSize);
			vTaskDelay(pdMS_TO_TICKS(10));

			dataModel_t info = dataHandler.getInfo();
			communicationHandler.write(reinterpret_cast<uint8_t*>(&info), sizeof(info));
		}
		else
		{
			vTaskDelay(COMMUNICATION_IDLE_DELAY);
		}
	}
}

static void controlLoop(void* pvParameters)
{
	Controller* localController = static_cast<Controller*>(pvParameters);

	while (true)
	{
		if (localController != nullptr)
		{
			localController->update();
		}
	}
}

static void testLoop(void* pvParameters)
{
	(void)pvParameters;

	if (ENABLE_COM_TEST)
	{
		testRunner.runComTest();
	}
	else if (ENABLE_TEST)
	{
		testRunner.runTests();
	}

	while (true)
	{
		vTaskDelay(TEST_LOOP_DELAY);
	}
}

static void pressureUpdateLoop(void* pvParameters)
{
	PressureTaskContext* context = static_cast<PressureTaskContext*>(pvParameters);

	while (true)
	{
		if (context != nullptr)
		{
			for (uint8_t i = 0; i < MAX_TOOLHEAD; ++i)
			{
				if (context->pressureSensor[i] != nullptr)
				{
					context->pressureSensor[i]->update();
				}
			}
		}

		vTaskDelay(PRESSURE_LOOP_DELAY);
	}
}
}

void setup()
{
	Serial.begin(SERIAL_BAUD_RATE);
	delay(SERIAL_STARTUP_DELAY_MS);
	while (!Serial)
	{
		delay(10);
	}

	initializeHardware();
	registerCommands();

	if (ENABLE_TEST)
	{
		xTaskCreatePinnedToCore(testLoop, "testTask", TEST_TASK_STACK, &controller, 1, nullptr, 1);
		xTaskCreatePinnedToCore(pressureUpdateLoop, "pressureTask", PRESSURE_TASK_STACK, &pressureTaskContext, 2, nullptr, 0);
	}
	else if (ENABLE_COM_TEST)
	{
		xTaskCreatePinnedToCore(testLoop, "testTask", TEST_TASK_STACK, &controller, 1, nullptr, 1);
		xTaskCreatePinnedToCore(communicationLoop, "communicationTask", COMMUNICATION_TASK_STACK, &controller, 1, nullptr, 0);
		xTaskCreatePinnedToCore(pressureUpdateLoop, "pressureTask", PRESSURE_TASK_STACK, &pressureTaskContext, 2, nullptr, 0);
	}
	else
	{
		xTaskCreatePinnedToCore(communicationLoop, "communicationTask", COMMUNICATION_TASK_STACK, &controller, 1, nullptr, 0);
		xTaskCreatePinnedToCore(pressureUpdateLoop, "pressureTask", PRESSURE_TASK_STACK, &pressureTaskContext, 2, nullptr, 0);
		xTaskCreatePinnedToCore(controlLoop, "controlTask", CONTROL_TASK_STACK, &controller, 1, nullptr, 1);
	}
}

void loop()
{
}