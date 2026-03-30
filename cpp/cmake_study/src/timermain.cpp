#include <string>
#include "timer.h"
#include <vector>
#include <iostream>

int main() {
    std::string word = "hello word!";
    std::vector<long long> timer;
    timer = times(word);
    long long sum = 0;
    sum = sumtime(timer);
    std::cout << "alltime: " << sum << "ns\n";
    meantime(timer, sum);
    MaxorMintime(timer);
    return 0;
}