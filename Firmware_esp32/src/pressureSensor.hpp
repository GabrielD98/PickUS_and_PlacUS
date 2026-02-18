#include <stdint.h>


class PressureSensor
{
	public:
		PressureSensor(uint8_t clkPin, uint8_t dataPin);
		void init();
		float getPressureKPa();

	private:
		long getRawPressure();
		uint8_t clkPin;
		uint8_t dataPin;
		long zeroValue;

};