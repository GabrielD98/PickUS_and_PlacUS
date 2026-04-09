#include "DataModel.h"

DataModel::DataModel() 
{
    dataModel = 
    {
        {
            CommandId::EMPTY,       /// Command id
            0,                      /// Command velocity (mm/s and degree/ss)
            {}                      /// Command requested position (mm and degrees) {0,0,0,0})
        },                      
        {},                     /// Current position (steps) {0,0,0,0}
        MachineState::READY     /// State 
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
