#include <gtest/gtest.h>

#include <algorithm>
#include <cstdint>
#include <cstring>
#include <vector>

#include "Arduino.h"
#include "CommunicationHandler.h"

namespace
{
class FakeStream : public Stream
{
public:
    std::size_t available() override
    {
        return readBuffer.size() - readPos;
    }

    std::size_t readBytes(uint8_t* buffer, std::size_t length) override
    {
        std::size_t toRead = std::min(length, available());
        if (toRead > 0)
        {
            std::memcpy(buffer, readBuffer.data() + readPos, toRead);
            readPos += toRead;
        }
        return toRead;
    }

    std::size_t write(const uint8_t* buffer, std::size_t length) override
    {
        written.insert(written.end(), buffer, buffer + length);
        return length;
    }

    void pushReadData(const std::vector<uint8_t>& data)
    {
        readBuffer.insert(readBuffer.end(), data.begin(), data.end());
    }

    std::vector<uint8_t> written;

private:
    std::vector<uint8_t> readBuffer;
    std::size_t readPos{0};
};

uint16_t computeChecksum(const std::vector<uint8_t>& payload)
{
    uint32_t sum = 0;
    for (uint8_t value : payload)
    {
        sum += value;
    }
    return static_cast<uint16_t>(sum & 0xFFFF);
}

std::vector<uint8_t> buildPacket(const std::vector<uint8_t>& payload, uint16_t checksumOverride = 0)
{
    ComHeader header{};
    header.magicNumber = MAGIC_NUMBER;
    header.payloadSize = static_cast<uint16_t>(payload.size());
    header.checkSum = checksumOverride ? checksumOverride : computeChecksum(payload);

    std::vector<uint8_t> packet(sizeof(ComHeader) + payload.size());
    std::memcpy(packet.data(), &header, sizeof(ComHeader));
    if (!payload.empty())
    {
        std::memcpy(packet.data() + sizeof(ComHeader), payload.data(), payload.size());
    }
    return packet;
}
}

TEST(CommunicationHandlerTest, ReadsValidPacket)
{
    FakeStream stream;
    CommunicationHandler handler(&stream);

    std::vector<uint8_t> payload{0x10, 0x20, 0x30};
    stream.pushReadData(buildPacket(payload));

    uint8_t outPayload[MAX_PAYLOAD_SIZE] = {};
    uint16_t payloadSize = 0;

    EXPECT_TRUE(handler.handleIncoming(outPayload, payloadSize));
    EXPECT_EQ(payloadSize, payload.size());
    EXPECT_TRUE(std::equal(payload.begin(), payload.end(), outPayload));
}

TEST(CommunicationHandlerTest, RejectsBadChecksum)
{
    FakeStream stream;
    CommunicationHandler handler(&stream);

    std::vector<uint8_t> payload{0xAA, 0xBB};
    stream.pushReadData(buildPacket(payload, 0xFFFF));

    uint8_t outPayload[MAX_PAYLOAD_SIZE] = {};
    uint16_t payloadSize = 0;

    EXPECT_FALSE(handler.handleIncoming(outPayload, payloadSize));
}

TEST(CommunicationHandlerTest, WritesHeaderAndPayload)
{
    FakeStream stream;
    CommunicationHandler handler(&stream);

    std::vector<uint8_t> payload{0x01, 0x02, 0x03, 0x04};
    handler.write(payload.data(), static_cast<uint16_t>(payload.size()));

    ASSERT_GE(stream.written.size(), sizeof(ComHeader) + payload.size());

    ComHeader header{};
    std::memcpy(&header, stream.written.data(), sizeof(ComHeader));

    EXPECT_EQ(header.magicNumber, MAGIC_NUMBER);
    EXPECT_EQ(header.payloadSize, payload.size());
    EXPECT_EQ(header.checkSum, computeChecksum(payload));

    std::vector<uint8_t> writtenPayload(stream.written.begin() + sizeof(ComHeader), stream.written.end());
    EXPECT_EQ(writtenPayload, payload);
}
