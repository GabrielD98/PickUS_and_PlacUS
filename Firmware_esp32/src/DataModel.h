/**
 * @file dataModel.h
 * @author PickusAndPlacus
 * @brief Class to control a shared chain of data between the Controller and the Interface.
 * @version 1.0
 * @date 17/04/2026
 */

#ifndef DATAMODEL_H
#define DATAMODEL_H

#include "../lib/data.hpp"
#include <mutex>

/**
 * @brief Chain of data used to exchange information.
 */
typedef struct dataModel
{
    command_t command;
    positionCartesian_t position;
    MachineState state;

}dataModel_t;

/**
 * @brief Allows protected exchange of information through a chain of data.
 */
class DataModel
{   
    public :
        /**
         * @brief Initializes the chain of data
         */
        DataModel();

        /**
         * @brief Protects the chain of data with a mutex.
         * @return Pointer adress to the chain of data.
         */
        dataModel_t* get();

        /**
         * @brief Release the mutex on the chain of data.
         */
        void release();

    private :
        // Chain of data accessible to both Controller and Interface to exchange informations and commands.
        dataModel_t dataModel;
        // Mutex to lock the chain of data while used.
        std::mutex mutex_; 
};

#endif