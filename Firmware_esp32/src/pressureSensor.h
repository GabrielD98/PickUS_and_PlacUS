/**
 * @file pressureSensor.h
 * @author PickusAndPlacus
 * @brief 
 * @version
 * @date
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
		 * @param clkPin 
		 * @param dataPin 
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