#include<chrono>
#include"timer.h"

Timer::Timer():start(std::chrono::steady_clock::now()){}

double Timer::timer_gap()const{
    auto end = std::chrono::steady_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    return duration.count();
}

