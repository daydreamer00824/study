#pragma once

#include<filesystem>
#include<vector>
std::vector<std::filesystem::path> config_path(const std::filesystem::path &config);
void forprint(const std::vector<std::filesystem::path> &path);