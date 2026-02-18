#ifndef DATAMODEL_H
#define DATAMODEL_H

#include "../lib/data.hpp"
#include <mutex>

typedef struct dataModel
{
    command_t command;
    position_t position;
    MachineState state;

}dataModel_t;


class DataModel
{   
    public :
        DataModel();
        dataModel_t* get();
        void release();
    private :
        dataModel_t dataModel;
        std::mutex mutex_; 
};

#endif