#include <gtest/gtest.h>

#include <cstring>
#include <vector>

#include "CommandHandler.h"
#include "commands/Command.h"

namespace
{
class DummyCommand : public Command
{
public:
    void prepare() override
    {
        prepared = true;
    }

    CommandState run() override
    {
        ++runCalls;
        return CommandState::Done;
    }

    bool setPayload(uint8_t* payload, uint16_t payloadSize) override
    {
        (void)payload;
        lastPayloadSize = payloadSize;
        setPayloadCalled = true;
        return true;
    }

    bool prepared = false;
    int runCalls = 0;
    uint16_t lastPayloadSize = 0;
    bool setPayloadCalled = false;
};

std::vector<uint8_t> buildFrame(uint8_t commandId, uint32_t commandNumber, const std::vector<uint8_t>& payload)
{
    CommmandFrameHeader header{commandId, commandNumber, static_cast<uint16_t>(payload.size())};
    std::vector<uint8_t> frame(sizeof(header) + payload.size());
    std::memcpy(frame.data(), &header, sizeof(header));
    if (!payload.empty())
    {
        std::memcpy(frame.data() + sizeof(header), payload.data(), payload.size());
    }
    return frame;
}
}

TEST(CommandHandlerTest, ConsumesPendingCommandOnce)
{
    CommandHandler handler;
    DummyCommand command;

    ASSERT_TRUE(handler.registerCommand(&command));

    auto frame = buildFrame(0, 1, {});
    EXPECT_TRUE(handler.setCurrentCommand(frame.data(), static_cast<uint16_t>(frame.size())));
    EXPECT_TRUE(handler.hasNewCommand());

    Command* selected = nullptr;
    EXPECT_TRUE(handler.tryGetNextCommand(selected));
    EXPECT_EQ(selected, &command);
    EXPECT_FALSE(handler.hasNewCommand());

    selected = nullptr;
    EXPECT_FALSE(handler.tryGetNextCommand(selected));
}

TEST(CommandHandlerTest, DuplicateCommandNumberIsIgnored)
{
    CommandHandler handler;
    DummyCommand command;

    ASSERT_TRUE(handler.registerCommand(&command));

    auto frame = buildFrame(0, 42, {});
    EXPECT_TRUE(handler.setCurrentCommand(frame.data(), static_cast<uint16_t>(frame.size())));

    Command* selected = nullptr;
    EXPECT_TRUE(handler.tryGetNextCommand(selected));
    EXPECT_EQ(selected, &command);

    EXPECT_TRUE(handler.setCurrentCommand(frame.data(), static_cast<uint16_t>(frame.size())));
    EXPECT_FALSE(handler.hasNewCommand());
}

TEST(CommandHandlerTest, RejectsInvalidFrameSize)
{
    CommandHandler handler;
    DummyCommand command;

    ASSERT_TRUE(handler.registerCommand(&command));

    std::vector<uint8_t> frame(sizeof(CommmandFrameHeader));
    CommmandFrameHeader header{0, 1, 2};
    std::memcpy(frame.data(), &header, sizeof(header));

    EXPECT_FALSE(handler.setCurrentCommand(frame.data(), static_cast<uint16_t>(frame.size())));
}
