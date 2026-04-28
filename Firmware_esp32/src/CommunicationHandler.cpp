#include "CommunicationHandler.h"

CommunicationHandler::CommunicationHandler(Stream* stream, DataHandler* dataHandler, 
                                             CommandHandler* commandHandler)
    : stream(stream), dataHandler(dataHandler), commandHandler(commandHandler)
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

void CommunicationHandler::handleIncoming()
{
    if (stream != nullptr && dataHandler != nullptr && commandHandler != nullptr)
	{
		ComHeader header;
		if (readHeader(header))
		{
			if (header.payloadSize < MAX_PAYLOAD_SIZE)
			{
				uint8_t payload[MAX_PAYLOAD_SIZE] = {0};
				if (header.payloadSize > 0)
				{
					if (!readPayload(payload, header.payloadSize))
						return;
				}
			
				// Validate checksum (sum of payload bytes)
				uint16_t computed = computeChecksum(payload, header.payloadSize);
				if (computed == header.checkSum)
				{
					commandHandler->setCurrentCommand(header.commandId, payload, header.payloadSize, header.commandNumber);
				}

			}

		}
			
		// Reply with a status frame built from the DataHandler snapshot
		writeStatus();
	}
}

void CommunicationHandler::writeStatus()
{
	if (stream != nullptr && dataHandler != nullptr)
	{
		// Prepare payload (copy snapshot)
		const uint8_t* payload = (const uint8_t *)&dataHandler->getInfo();
		uint16_t payloadSize = (uint16_t)sizeof(dataModel_t);

		// Build output header (status reply). Use 0xFF as default status commandId.
		ComHeader outHeader;
		outHeader.magicNumber = MAGIC_NUMBER;
		outHeader.commandId = 0xFF;
		outHeader.commandNumber = 0;
		outHeader.payloadSize = payloadSize;
		outHeader.checkSum = computeChecksum(payload, payloadSize);

		// Send header then payload
		stream->write((const uint8_t *)(&outHeader), sizeof(ComHeader));
		stream->write(payload, payloadSize);
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
