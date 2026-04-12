#pragma once
#include<chrono>

class Timer{
    public:
        Timer();

        double timer_gap() const;

    private:
        std::chrono::steady_clock::time_point start;
};