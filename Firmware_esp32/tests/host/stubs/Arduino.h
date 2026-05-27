#pragma once

#include <cstdint>
#include <cstddef>

class Stream
{
public:
	virtual ~Stream() = default;

	virtual std::size_t available()
	{
		return 0;
	}

	virtual std::size_t readBytes(uint8_t* buffer, std::size_t length)
	{
		(void)buffer;
		(void)length;
		return 0;
	}

	virtual std::size_t write(const uint8_t* buffer, std::size_t length)
	{
		(void)buffer;
		return length;
	}
};

extern Stream Serial;

uint64_t millis();
void setMillis(uint64_t value);
