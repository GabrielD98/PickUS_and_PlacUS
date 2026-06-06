#pragma once

class AccelStepper
{
public:
    void setMaxSpeed(float value)
    {
        maxSpeed = value;
    }

    void setSpeed(float value)
    {
        speed = value;
    }

    void runSpeed()
    {
        ++runSpeedCalls;
    }

    long currentPosition() const
    {
        return position;
    }

    void setCurrentPosition(long value)
    {
        position = value;
    }

    float getMaxSpeed() const
    {
        return maxSpeed;
    }

    float getSpeed() const
    {
        return speed;
    }

    int getRunSpeedCalls() const
    {
        return runSpeedCalls;
    }

private:
    long position{0};
    float maxSpeed{0.0f};
    float speed{0.0f};
    int runSpeedCalls{0};
};
