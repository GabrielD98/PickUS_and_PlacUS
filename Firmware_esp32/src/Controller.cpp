#include "controller.h"


#define POSITION_UPDATE_FREQ 100    // ms

Controller::Controller(CommandHandler* commandHandler)
    : commandHandler(commandHandler), machineState(MachineState::Ready), lastDataUpdateMS(millis())
{
}


void Controller::update()
{
    switch (machineState)
    {
        case MachineState::Error:
            //TODO
            break;
        
        case MachineState::Ready:
        {
            Command* nextCommand = nullptr;
            if (commandHandler->tryGetNextCommand(nextCommand))
            {
                nextCommand->prepare();
                machineState = MachineState::Running;
            }
            break;   
        }
            
        case MachineState::Running: 
        {
            Command* currentCommand = commandHandler->getCurrentCommand();
            if (currentCommand == nullptr)
            {
                machineState = MachineState::Error;
                break;
            }

            switch (currentCommand->run())
            {
                    case CommandState::Done:
                        machineState = MachineState::Ready;
                        break;
                    
                    case CommandState::InProgress:
                        machineState = MachineState::Running;
                        break;
                    
                    case CommandState::Error:
                        machineState = MachineState::Error;
                        break;

            }
            break;   
                }
    }


    // Limiting information updating rate
    if((millis() - lastDataUpdateMS) >= 1000 / POSITION_UPDATE_FREQ)
    {
        //TODO: Add data update (position,command id, p sensor)
    }
}


