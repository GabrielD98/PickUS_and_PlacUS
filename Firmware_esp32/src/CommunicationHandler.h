/**
 * @file CommunicationHandler.h
 * @brief Serial communication handling for framed packets.
 */
#ifndef COMMUNICATIONHANDLER_H
#define COMMUNICATIONHANDLER_H

#include <Arduino.h>
#include "../lib/data.hpp"

constexpr uint16_t MAGIC_NUMBER =  0xFACE;
#define MAX_PAYLOAD_SIZE 256  // Maximum size of a command payload

struct __attribute__((packed)) ComHeader 
{
	uint16_t magicNumber;
	uint16_t checkSum;
	uint16_t payloadSize;

};

class CommunicationHandler
{
public:
    /**
     * @brief Construct a new Communication Handler
     * @param stream Stream used for read/write (defaults to global Serial)
     */
    CommunicationHandler(Stream* stream = &Serial);

    /**
     * @brief Try to read a communication header from the stream.
     *
        * Reads a ComHeader struct containing magic number, checksum, and payload size.
        * Validates the magic number; checksum is validated in handleIncoming().
     *
     * @param header Output struct to populate.
     * @return true when a full valid header was read and populated, false otherwise.
     */
    bool readHeader(ComHeader &header);

    /**
     * @brief Read a payload of given size into buffer. Blocks until size read or returns false.
     */
    bool readPayload(uint8_t* buf, uint16_t size);

    /**
        * @brief Handle an incoming packet by reading the header, then the payload.
     *
        * Reads a ComHeader, validates it, then reads the variable-size payload and
        * copies it into the caller-provided buffer when non-null.
     *
        * @param payload Output buffer for the received payload bytes.
        * @param payloadSize In: ignored. Out: payload size in bytes when the packet is valid.
        * This is a convenience wrapper suitable for use from a task loop.
     */
    bool handleIncoming(uint8_t* payload, uint16_t &payloadSize);

    /**
        * @brief Write a framed payload back on the stream.
     * 
        * Sends a ComHeader followed by the payload bytes.
     */
    void write(uint8_t* msg, uint16_t size);

private:
    Stream* stream;

    /**
     * @brief Compute a simple byte sum checksum over data.
     *
     * @param data Pointer to data buffer.
     * @param size Size of data in bytes.
     * @return uint16_t Checksum (sum of all bytes, modulo 65536).
     */
    uint16_t computeChecksum(const uint8_t* data, uint16_t size);
};

#endif
