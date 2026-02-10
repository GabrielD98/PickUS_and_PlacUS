#include <Arduino.h>

#include "pressureSensor.hpp"
#include "assert.h"


PressureSensor::PressureSensor(uint8_t clkPin, uint8_t dataPin)
{
	this->clkPin = clkPin;
	this->dataPin = dataPin;
	this->zeroValue = 0;
	pinMode(clkPin, OUTPUT);
	pinMode(dataPin, INPUT);
}

long PressureSensor::getRawPressure()
{
	  long result = 0;

  // Wait for the module to be ready 
  while (digitalRead(this->dataPin) == HIGH); //TODO: Add a timeout 

  // Read 24-bit data
  for (int i = 0; i < 24; i++) {
    digitalWrite(this->clkPin, HIGH);
    result = (result << 1) | digitalRead(this->dataPin);
    digitalWrite(this->clkPin, LOW);
  }

  // Apply clock pulse to complete the conversion
  digitalWrite(this->clkPin, HIGH);
  delayMicroseconds(1);
  digitalWrite(this->clkPin, LOW);

  // Handle 24-bit signed integer (two's complement)
  // If bit 23 is set, sign-extend to fill the higher bits
  if (result & 0x800000) {  // Check if sign bit (bit 23) is set
    result |= 0xFF000000;   // Sign extend: set bits 24-31 to 1
  }

  return result;

}

void PressureSensor::init()
{
	this->zeroValue = this->getRawPressure();
}


float PressureSensor::getPressureKPa()
{
	assert(this->zeroValue != 0);

	long pressureValue = this->getRawPressure();
	// Calculate differential from zero reading (which is at 101.3 kPa)
	// Convert to kPa: 24-bit range (16777216) covers 40 kPa
	float differential = (pressureValue - this->zeroValue) * (40.0 / 16777216.0);
	float pressureKPa = 101.3 + differential;

	return pressureKPa;

}
