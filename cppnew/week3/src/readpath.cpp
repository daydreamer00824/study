#include<vector>
#include<iostream>
#include<filesystem>
#include<stdexcept>
#include"readpath.h"
#include<string>

std::vector<std::filesystem::path> image_path(const std::string &input){
    if(!std::filesystem::exists(input) || !std::filesystem::is_directory(input)){
        throw std::runtime_error("not exists or not directory");
    }
    std::vector<std::filesystem::path> path;

    for(const auto & p : std::filesystem::directory_iterator(input)){
        if(!std::filesystem::is_regular_file(p.path())){
            throw std::runtime_error("not file");
        }
        path.push_back(p.path());
    }
    return path;
}