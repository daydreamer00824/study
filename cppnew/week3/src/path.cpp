#include<filesystem>
#include<stdexcept>
#include<fstream>
#include<vector>
#include<iostream>
#include"path.h"

std::vector<std::filesystem::path> config_path(const std::filesystem::path &configs){
    std::ifstream read_txt(configs);
    if(!read_txt.is_open()){
        throw std::runtime_error("配置文件不存在");
    }
    std::string line;
    std::vector<std::filesystem::path> config;
    while (std::getline(read_txt, line))
    {
        config.push_back(line);
    }
    return config;
}

void forprint(const std::vector<std::filesystem::path> &path){
    if(path.empty()){
        throw std::runtime_error("empty");
    }
    for(const auto &p : path){
        std::cout << "path: " << p << std::endl;
    }
}