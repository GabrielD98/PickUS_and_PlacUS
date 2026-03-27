#include "Arduino.h"
#include "../lib/data.hpp"
#include "BoardConfig.h"
#include "Controller.h"
#include "Tests/TestRunner.h"

Controller ctrl;
TestRunner testRunner(&ctrl);

void communicationLoop(void *pvParameters);
void controlLoop(void *pvParameters);
void testLoop(void *pvParameters);

void setup()
{
	
	Serial.begin(115200);
	delay(3000);
	while (!Serial) { delay(10); } // Block until host opens the serial port
	if(ENABLE_TEST)
	{
		xTaskCreatePinnedToCore(
			testLoop,
			"testTask",
			10000,
			&ctrl,
			1,
			NULL,
			1
		);
	}
	else if(ENABLE_COM_TEST)
	{
		xTaskCreatePinnedToCore(
			testLoop,
			"testTask",
			10000,
			&ctrl,
			1,
			NULL,
			1
		);

		xTaskCreatePinnedToCore(
			communicationLoop,
			"communicationTask",
			10000,
			&ctrl,
			1,
			NULL,
			0
		);
	}
	else
	{
		xTaskCreatePinnedToCore(
			communicationLoop,
			"communicationTask",
			10000,
			&ctrl,
			1,
			NULL,
			0
		);

		xTaskCreatePinnedToCore(
			controlLoop,
			"controlTask",
			10000,
			&ctrl,
			1,
			NULL,
			1
		);
	}
	

}


void loop()
{
}


/**
 * @brief FreeRTOS task that handles serial communication with the host.
 *        Receives a command_t packet and writes it to the shared DataModel,
 *        then reads back the current state and position and sends a statusFrame_t reply.
 *
 * @param pvParameters Pointer to the shared Controller instance.
 */
void communicationLoop(void *pvParameters)
{
	Controller* controller = (Controller*)pvParameters;
	while(true)
	{
		if(Serial.available() >= sizeof(command_t))
		{
			command_t receiveCmd;
			uint8_t byteBuffer[sizeof(command_t)];
	
			//Receive section
			Serial.readBytes(byteBuffer, sizeof(command_t));
			memcpy(&receiveCmd, byteBuffer, sizeof(command_t));
			dataModel_t* dataModel = controller->dataModel.get();
			dataModel->command = receiveCmd;
			controller->dataModel.release();

			vTaskDelay(pdMS_TO_TICKS(50)); //TODO: Confirm this delay
			
			//Send section
			statusFrame_t statusFrame;
			dataModel = controller->dataModel.get();
			statusFrame.position = dataModel->position;
			statusFrame.state = dataModel->state;
			controller->dataModel.release();
			Serial.write((const uint8_t *)&statusFrame, sizeof(statusFrame_t));
		}
		else
		{
			vTaskDelay(10);
		}
	}
}


/**
 * @brief FreeRTOS task that runs the main motion control loop.
 *        Calls Controller::update() continuously to process commands
 *        from the shared DataModel and drive the stepper motors.
 *
 * @param pvParameters Pointer to the shared Controller instance.
 */
void controlLoop(void *pvParameters)
{
	Controller* controller = (Controller*)pvParameters;
	while(1)
	{
		controller->update();
	}
}

/**
 * @brief FreeRTOS task used during integration testing (enabled via ENABLE_TEST build flag).
 *        Replaces controlLoop on core 1. Use this to exercise hardware and verify
 *        that communication, DataModel, and actuators behave as expected.
 *
 * @param pvParameters Pointer to the shared Controller instance.
 */
void testLoop(void*pvParameters)
{
	Controller* controller = (Controller*)pvParameters;
	
	if(ENABLE_COM_TEST)
	{
		testRunner.runComTest();
	}
	else if(ENABLE_TEST)
	{
		testRunner.runTests();
	}
	
	while(1)
	{
		vTaskDelay(100);
	}
}
