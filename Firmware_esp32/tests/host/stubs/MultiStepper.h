#pragma once

#include <array>

class MultiStepper
{
public:
    void moveTo(long* positions)
    {
        if (positions != nullptr)
        {
            targets[0] = positions[0];
            targets[1] = positions[1];
            targets[2] = positions[2];
            targets[3] = positions[3];
        }
        moveToCalls++;
    }

    bool run()
    {
        return runResult;
    }

    void setRunResult(bool value)
    {
        runResult = value;
    }

    std::array<long, 4> getTargets() const
    {
        return targets;
    }

    int getMoveToCalls() const
    {
        return moveToCalls;
    }

private:
    std::array<long, 4> targets{0, 0, 0, 0};
    bool runResult{false};
    int moveToCalls{0};
};
