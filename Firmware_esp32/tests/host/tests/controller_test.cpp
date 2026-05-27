#include <gtest/gtest.h>

#include <cstring>
#include <vector>

#include "Arduino.h"
#include "CommandHandler.h"
#include "Controller.h"
#include "DataHandler.h"
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
        (void)payloadSize;
        return true;
    }

    bool prepared = false;
    int runCalls = 0;
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

TEST(ControllerTest, RunsCommandAndPublishesState)
{
    CommandHandler handler;
    DummyCommand command;
    DataHandler dataHandler(nullptr, &handler);

    ASSERT_TRUE(handler.registerCommand(&command));

    setMillis(0);
    Controller controller(&handler, &dataHandler);

    auto frame = buildFrame(0, 1, {});
    EXPECT_TRUE(handler.setCurrentCommand(frame.data(), static_cast<uint16_t>(frame.size())));

    setMillis(20);
    controller.update();
    EXPECT_TRUE(command.prepared);
    dataModel_t info = dataHandler.getInfo();
    EXPECT_EQ(info.state, MachineState::Running);

    setMillis(40);
    controller.update();
    EXPECT_EQ(command.runCalls, 1);
    info = dataHandler.getInfo();
    EXPECT_EQ(info.state, MachineState::Ready);
}
