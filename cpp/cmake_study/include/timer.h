#pragma once
#include <vector>
#include <string>

std::vector<long long> times(const std::string &word);
long long sumtime(const std::vector<long long> &timer);
void meantime(const std::vector<long long> &timer, long long sum);
void MaxorMintime(const std::vector<long long> &times);