#include<iostream>
#include<filesystem>
#include<vector>
#include"image.h"

int main(int argc, char *argv[]){
    if(argc < 3){
        std::cerr << "error shuru" << std::endl;
        return 1;
    }

    std::filesystem::path input = argv[1];
    std::filesystem::path output = argv[2];
    std::vector<std::filesystem::path> file_path;

    try{
        Imageprocess image(224, 224);
        file_path = image.image_path(input);
        for (const auto &p : file_path){
            std::cout << "file: " << p << std::endl;
        }
        image.process(file_path, output);
    }
    catch(const std::exception &e){
        std::cerr << e.what() << std::endl;
        return 1;
    }
    return 0;
}