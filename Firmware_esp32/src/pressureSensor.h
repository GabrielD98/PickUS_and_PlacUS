/**
 * @file pressureSensor.h
 * @author PickusAndPlacus
 * @brief Class to convert and interpret data from a pressure sensor.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef PRESSURESENSOR_H
#define PRESSURESENSOR_H

#include <stdint.h>

/**
 * @brief 
 * 
 */
class PressureSensor
{
	public:
		/**
		 * @brief 
		 * @param clkPin Sensor clock pin.
		 * @param dataPin Sensor output pin.
		 */
		PressureSensor(uint8_t clkPin, uint8_t dataPin);
		
		/**
		 * @brief 
		 */
		void init();

		/**
		 * @brief
		 * @return 
		 */
		float getPressureKPa();

	private:
		/**
		 * @brief
		 * @return 
		 */
		long getRawPressure();

		/**
		 * @brief 
		 */
		uint8_t clkPin;

		/**
		 * @brief 
		 */
		uint8_t dataPin;

		/**
		 * @brief 
		 */
		long zeroValue;

};

#endif