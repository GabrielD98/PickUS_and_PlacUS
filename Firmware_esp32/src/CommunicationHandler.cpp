#include "CommunicationHandler.h"
#include <cstring>

CommunicationHandler::CommunicationHandler(Stream* stream)
    : stream(stream)
{
}

bool CommunicationHandler::readHeader(ComHeader &header)
{
    bool result = false;

    if (stream != nullptr && stream->available() >= (int)sizeof(ComHeader))
    {
        uint8_t b0 = 0;
        uint8_t b1 = 0;
        bool    aligned = false;

        // Sliding-window realignment: scan until magic number is found
        // or not enough bytes remain
        while (!aligned && stream->available() >= (int)sizeof(ComHeader))
        {
            b0 = (uint8_t)stream->read();

            if (b0 == (uint8_t)(MAGIC_NUMBER & 0xFF))
            {
                b1 = (uint8_t)stream->peek();

                uint16_t candidate = (uint16_t)(b0 | (b1 << 8));
                if (candidate == MAGIC_NUMBER)
                {
                    stream->read(); // consume b1
                    aligned = true;
                }
            }
        }

		if (aligned)
		{
			uint8_t buf[sizeof(ComHeader)];
			
			size_t remaining = sizeof(ComHeader) - sizeof(uint16_t);
			
			if (stream->readBytes(buf, remaining) == remaining)
			{
				header.magicNumber = MAGIC_NUMBER;
				memcpy(&header.checkSum, buf, remaining);
				result = (header.payloadSize < MAX_PAYLOAD_SIZE);
			}
		}
    }

    return result;
}

bool CommunicationHandler::readPayload(uint8_t* buf, uint16_t size, uint16_t checkSum)
{
	bool result = false;
    if (stream != nullptr && buf != nullptr)
	{
		size_t read = stream->readBytes(buf, (size_t)size);
		result = (read == (size_t)size) && computeChecksum(buf, checkSum);
	}
	return result;
}

void CommunicationHandler::write(uint8_t* msg, uint16_t size)
{
	if (stream != nullptr)
	{
		// Build output header (status reply). Use 0xFF as default status commandId.
		ComHeader outHeader;
		outHeader.magicNumber = MAGIC_NUMBER;
		outHeader.payloadSize = size;
		outHeader.checkSum = computeChecksum(msg, size);

		// Send header then payload
		stream->write((const uint8_t *)(&outHeader), sizeof(ComHeader));
		stream->write(msg, size);
	}

}

uint16_t CommunicationHandler::computeChecksum(const uint8_t* data, uint16_t size)
{
	uint32_t sum = 0;

	if (data != nullptr && size != 0)
	{
		for (uint16_t i = 0; i < size; ++i)
		{
			sum += data[i];
		}
	}
    // Return lower 16 bits as the checksum
    return (uint16_t)(sum & 0xFFFF);
}
