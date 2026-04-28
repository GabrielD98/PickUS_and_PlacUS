/**
 * @file CommunicationHandler.h
 * @brief Skeleton for serial communication handling (header/payload + status reply)
 */
#ifndef COMMUNICATIONHANDLER_H
#define COMMUNICATIONHANDLER_H

#include <Arduino.h>
#include "../lib/data.hpp"
#include "DataHandler.h"

constexpr uint16_t MAGIC_NUMBER =  0xFACE;
#define MAX_PAYLOAD_SIZE 256  // Maximum size of a command payload


struct __attribute__((packed)) ComHeader 
{
	uint16_t magicNumber;
	uint16_t checkSum;
	uint8_t commandId;
	uint32_t commandNumber;
	uint16_t payloadSize;

};

class CommunicationHandler
{
public:
    /**
     * @brief Construct a new Communication Handler
     * @param stream Stream used for read/write (defaults to global Serial)
     * @param dataHandler Pointer to the DataHandler for reading/writing shared state
     * @param commandHandler Pointer to the CommandHandler for dispatching commands
     */
    CommunicationHandler(Stream* stream = &Serial, DataHandler* dataHandler = nullptr, 
                         CommandHandler* commandHandler = nullptr);

    /**
     * @brief Try to read a communication header from the stream.
     *
     * Reads a ComHeader struct containing magic number, checksum, command ID,
     * and payload size. Validates the magic number; checksum is validated in handleIncoming().
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
     * @brief Handle an incoming packet: read header, then payload (if size > 0),
     * and reply with status information from the stored DataHandler.
     *
     * Reads a ComHeader, validates it, then reads the variable-size payload.
     * Finally, replies with a status frame built from the latest DataModel snapshot.
     *
     * This is a convenience wrapper suitable for use from a task loop.
     */
    void handleIncoming();

    /**
     * @brief Write complete dataModel information back on the stream.
     * 
     * Sends all last info from dataHandler: state, currentCommandId, position (steps),
     * pressure array, valve states, and pump state.
     */
    void writeStatus();

private:
    Stream* stream;
    DataHandler* dataHandler;
    CommandHandler* commandHandler;

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
