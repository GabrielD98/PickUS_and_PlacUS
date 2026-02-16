#include "DataModel.h"

DataModel::DataModel() 
{
    dataModel = 
    {
        {CommandId::EMPTY, 0, {}},  //Command (command, velocity, position)
        {},                         //Position {0,0,0,0}
        MachineState::READY         //State 
    };
}


// Stoke comand position and machine state 
dataModel_t* DataModel::get()
{
    mutex_.lock();
    return &dataModel;
}


void DataModel::release()
{
    mutex_.unlock();
}
