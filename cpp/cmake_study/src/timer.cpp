#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <algorithm>

std::vector<long long> times(const std::string &word) {
    std::vector<long long> timer;
    timer.reserve(100);
    std::cout << timer.capacity() << '\n';

    for (int i = 0; i < 100; i++) {
        std::string temp = word;
        auto start = std::chrono::steady_clock::now();
        temp += 'h';

        auto end = std::chrono::steady_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
        timer.push_back(duration.count());
    }

    return timer;
}

long long sumtime(const std::vector<long long> &timer) {
    long long sum = 0;
    for (const auto &t : timer) {
        sum += t;
    }
    return sum;
}

void meantime(const std::vector<long long> &timer, long long sum) {
    if(timer.empty()) {
        return ;
    }
    std::cout << "menatime:" << static_cast<double>(sum) / timer.size() << "ns\n";
}

void MaxorMintime(const std::vector<long long> &times) {
    if(times.empty()) {
        return ;
    }
    auto max = *std::max_element(times.begin(), times.end());
    auto min = *std::min_element(times.begin(), times.end());
    std::cout << "maxtime" << max << "ns  " << "min" << min << "ns" <<"\n";
}

