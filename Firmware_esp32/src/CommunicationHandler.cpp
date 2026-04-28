#include "CommunicationHandler.h"

CommunicationHandler::CommunicationHandler(Stream* stream)
    : stream(stream)
{
}

bool CommunicationHandler::readHeader(ComHeader &header)
{
	bool result = false;

	if (stream != nullptr)
	{
		size_t needed = sizeof(ComHeader);
		if ((size_t)stream->available() >= needed)
		{
			uint8_t buf[sizeof(ComHeader)];
			size_t read = stream->readBytes(buf, needed);
			if (read == needed)
			{
				memcpy(&header, buf, sizeof(ComHeader));
				// Validate magic number
				if (header.magicNumber == MAGIC_NUMBER)
				{
					result = true;
				}
			}
		}
	}

	return result;
}

bool CommunicationHandler::readPayload(uint8_t* buf, uint16_t size)
{
    if (stream == nullptr || buf == nullptr) return false;
	size_t read = stream->readBytes(buf, (size_t)size);
	return (read == (size_t)size);
}

bool CommunicationHandler::handleIncoming(uint8_t* payload, uint16_t &payloadSize)
{
	bool result = false;

    if (stream != nullptr)
	{
		ComHeader header;
		if (readHeader(header))
		{
			if (header.payloadSize < MAX_PAYLOAD_SIZE)
			{
				uint8_t receivedPayload[MAX_PAYLOAD_SIZE] = {0};
				if (header.payloadSize > 0)
				{
					if (!readPayload(receivedPayload, header.payloadSize))
						return result;
				}
			
				// Validate checksum (sum of payload bytes)
				uint16_t computed = computeChecksum(receivedPayload, header.payloadSize);
				if (computed == header.checkSum)
				{
					if (payload != nullptr)
					{
						memcpy(payload, receivedPayload, header.payloadSize);
					}
					payloadSize = header.payloadSize;
					result = true;
				}

			}

		}
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
