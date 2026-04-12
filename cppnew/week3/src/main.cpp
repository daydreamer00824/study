#include<iostream>
#include<filesystem>
#include<stdexcept>
#include<vector>
#include<filesystem>
#include"timer.h"
#include"path.h"
#include"readpath.h"

int main(){
    
    std::filesystem::path config = "/home/daydreamer/Desktop/study/cppnew/week3/include/config.txt";

    try{
        Timer timer;
        std::vector<std::filesystem::path> allpath;
        std::string input;
        std::string output;
        std::vector<std::filesystem::path> filepath;
        allpath = config_path(config);
        input = allpath.at(0).string();
        output = allpath.at(1).string();
        filepath = image_path(input);
        forprint(filepath);
        double alltime = timer.timer_gap();
        std::cout << alltime << "ms" << std::endl;
    }
    catch(const std::exception &e){
        std::cout << e.what() << std::endl;
        return 1;
    }
    return 0;

}