#include <AccelStepper.h>
#include <Arduino.h>


void checkSerial();
void RunTheMotor();
void RotateRelative();
void RotateAbsolute();
void PrintCommands();
void GoHome();

//User-defined values
long receivedSteps = 0; //Number of steps
long receivedSpeed = 0; //Steps / second
long receivedAcceleration = 0; //Steps / second^2
char receivedCommand;
//-------------------------------------------------------------------------------
int directionMultiplier = 1; // = 1: positive direction, = -1: negative direction
bool newData, runallowed = false; // booleans for new data from serial, and runallowed flag
AccelStepper stepper(1, 4, 5);// direction Digital 9 (CCW), pulses Digital 8 (CLK)
 
void setup()
{
    Serial.begin(9600); //define baud rate
    Serial.println("Demonstration of AccelStepper Library"); //print a messages
    Serial.println("Send 'C' for printing the commands.");
 
    //setting up some default values for maximum speed and maximum acceleration
    Serial.println("Default speed: 400 steps/s, default acceleration: 800 steps/s^2.");
    stepper.setMaxSpeed(400); //SPEED = Steps / second
    stepper.setAcceleration(800); //ACCELERATION = Steps /(second)^2
 
    stepper.disableOutputs(); //disable outputs
}
 
void loop()
{
    //Constantly looping through these 2 functions.
    //We only use non-blocking commands, so something else (should also be non-blocking) can be done during the movement of the motor
 
    checkSerial(); //check serial port for new commands
    RunTheMotor(); //function to handle the motor  
 
}
 
 
void RunTheMotor() //function for the motor
{
    if (runallowed == true)
    {
        stepper.enableOutputs(); //enable pins
        stepper.run(); //step the motor (this will step the motor by 1 step at each loop)  
    }
    else //program enters this part if the runallowed is FALSE, we do not do anything
    {
        stepper.disableOutputs(); //disable outputs
        return;
    }
}
 
 
 
void checkSerial() //function for receiving the commands
{  
    if (Serial.available() > 0) //if something comes from the computer
    {
        receivedCommand = Serial.read(); // pass the value to the receivedCommad variable
        newData = true; //indicate that there is a new data by setting this bool to true
 
        if (newData == true) //we only enter this long switch-case statement if there is a new command from the computer
        {
            switch (receivedCommand) //we check what is the command
            {
 
            case 'P': //P uses the move() function of the AccelStepper library, which means that it moves relatively to the current position.              
               
                receivedSteps = Serial.parseFloat(); //value for the steps
                receivedSpeed = Serial.parseFloat(); //value for the speed
                directionMultiplier = 1; //We define the direction
                Serial.println("Positive direction."); //print the action
                RotateRelative(); //Run the function
 
                //example: P2000 400 - 2000 steps (5 revolution with 400 step/rev microstepping) and 400 steps/s speed
                //In theory, this movement should take 5 seconds
                break;         
 
            case 'N': //N uses the move() function of the AccelStepper library, which means that it moves relatively to the current position.      
               
                receivedSteps = Serial.parseFloat(); //value for the steps
                receivedSpeed = Serial.parseFloat(); //value for the speed 
                directionMultiplier = -1; //We define the direction
                Serial.println("Negative direction."); //print action
                RotateRelative(); //Run the function
 
                //example: N2000 400 - 2000 steps (5 revolution with 400 step/rev microstepping) and 500 steps/s speed; will rotate in the other direction
                //In theory, this movement should take 5 seconds
                break;
 
            case 'R': //R uses the moveTo() function of the AccelStepper library, which means that it moves absolutely to the current position.            
 
                receivedSteps = Serial.parseFloat(); //value for the steps
                receivedSpeed = Serial.parseFloat(); //value for the speed     
                directionMultiplier = 1; //We  the function
 
                //example: R800 400 - It moves to the position which is located at +800 steps away from 0.
                break;
 
            case 'r': //r uses the moveTo() function of the AccelStepper library, which means that it moves absolutely to the current position.            
 
                receivedSteps = Serial.parseFloat(); //value for the steps
                receivedSpeed = Serial.parseFloat(); //value for the speed 
                directionMultiplier = -1; //We define the direction
                Serial.println("Absolute position (-)."); //print the action
                RotateAbsolute(); //Run the function
 
                //example: r800 400 - It moves to the position which is located at -800 steps away from 0.
                break;
 
            case 'S': // Stops the motor
               
                stepper.stop(); //stop motor
                stepper.disableOutputs(); //disable power
                Serial.println("Stopped."); //print action
                runallowed = false; //disable running
                break;
 
            case 'A': // Updates acceleration
 
                runallowed = false; //we still keep running disabled, since we just update a variable
                stepper.disableOutputs(); //disable power
                receivedAcceleration = Serial.parseFloat(); //receive the acceleration from serial
                stepper.setAcceleration(receivedAcceleration); //update the value of the variable
                Serial.print("New acceleration value: "); //confirm update by message
                Serial.println(receivedAcceleration); //confirm update by message
                break;
 
            case 'L': //L: Location
 
                runallowed = false; //we still keep running disabled
                stepper.disableOutputs(); //disable power
                Serial.print("Current location of the motor: ");//Print the message
                Serial.println(stepper.currentPosition()); //Printing the current position in steps.
                break;
               
            case 'H': //H: Homing
 
                runallowed = true;     
                Serial.println("Homing"); //Print the message
                GoHome();// Run the function
                break;
 
            case 'U':
 
                runallowed = false; //we still keep running disabled
                stepper.disableOutputs(); //disable power
                stepper.setCurrentPosition(0); //Reset current position. "new home"            
                Serial.print("The current position is updated to: "); //Print message
                Serial.println(stepper.currentPosition()); //Check position after reset.
                break; 
 
            case 'C':
 
                PrintCommands(); //Print the commands for controlling the motor
                break;
 
            default:  

                break;
            }
        }
        //after we went through the above tasks, newData is set to false again, so we are ready to receive new commands again.
        newData = false;       
    }
}
 

void GoHome()
{  
    if (stepper.currentPosition() == 0)
    {
        Serial.println("We are at the home position.");
        stepper.disableOutputs(); //disable power
    }
    else
    {
        stepper.setMaxSpeed(400); //set speed manually to 400. In this project 400 is 400 step/sec = 1 rev/sec.
        stepper.moveTo(0); //set abolute distance to move
    }
}
 
void RotateRelative()
{
    //We move X steps from the current position of the stepper motor in a given direction.
    //The direction is determined by the multiplier (+1 or -1)
   
    runallowed = true; //allow running - this allows entering the RunTheMotor() function.
    stepper.setMaxSpeed(receivedSpeed); //set speed
    stepper.move(directionMultiplier * receivedSteps); //set relative distance and direction
}
 
 

void RotateAbsolute()
{
    //We move to an absolute position.
    //The AccelStepper library keeps track of the position.
    //The direction is determined by the multiplier (+1 or -1)
    //Why do we need negative numbers? - If you drive a threaded rod and the zero position is in the middle of the rod...
 
    runallowed = true; //allow running - this allows entering the RunTheMotor() function.
    stepper.setMaxSpeed(receivedSpeed); //set speed
    stepper.moveTo(directionMultiplier * receivedSteps); //set relative distance   
}
 

void PrintCommands()
{  
    //Printing the commands
    Serial.println(" 'C' : Prints all the commands and their functions.");
    Serial.println(" 'P' : Rotates the motor in positive (CW) direction, relative.");
    Serial.println(" 'N' : Rotates the motor in negative (CCW) direction, relative.");
    Serial.println(" 'R' : Rotates the motor to an absolute positive position (+).");
    Serial.println(" 'r' : Rotates the motor to an absolute negative position (-).");
    Serial.println(" 'S' : Stops the motor immediately."); 
    Serial.println(" 'A' : Sets an acceleration value.");
    Serial.println(" 'L' : Prints the current position/location of the motor.");
    Serial.println(" 'H' : Goes back to 0 position from the current position (homing).");
    Serial.println(" 'U' : Updates the position current position and makes it as the new 0 position. ");   
}