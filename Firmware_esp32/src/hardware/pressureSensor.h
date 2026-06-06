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
#include <mutex>

/**
 * @brief Converts and interprets raw data from a pressure sensor.
 */
class PressureSensor
{
	public:
		/**
		 * @brief Creates a PressureSensor object bound to the sensor pins.
		 * @param clkPin Sensor clock pin.
		 * @param dataPin Sensor output pin.
		 * @note Call init() before reading pressure values.
		 */
		PressureSensor(uint8_t clkPin, uint8_t dataPin);
		
		/**
		 * @brief Initializes the pressure sensor zero value, which is converted to 101.3 kPa.
		 * @note If this function is not called before requesting pressure in kPa, the program will assert.
		 */
		void init();

		/**
		 * @brief Update the cached pressure value from the raw sensor reading.
		 */
		void update();

		/**
		 * @brief Get the last cached pressure value in kPa.
		 * @return Pressure in kPa.
		 */
		float getPressureKPa();

	private:
		/**
		 * @brief Reads the raw pressure value from the sensor.
		 * @return Raw pressure reading.
		 */
		long getRawPressure();


		uint8_t clkPin;

		uint8_t dataPin;

		/**
		 * @brief Zero-pressure raw reference value.
		 */
		long zeroValue;

		/**
		 * @brief Last computed pressure value in kPa.
		 */
		float pressureKPa;

		/**
		 * @brief Protects pressureKPa and zeroValue during read/update operations.
		 */
		std::mutex mutex_;

};

#endif