#include<filesystem>
#include<vector>
#include<stdexcept>
#include<iostream>
#include<opencv2/opencv.hpp>
#include"image.h"

Imageprocess::Imageprocess(int w, int h):width(w), height(h){}

std::vector<std::filesystem::path> Imageprocess::image_path(const std::filesystem::path &input){
    if (!std::filesystem::exists(input) || !std::filesystem::is_directory(input))
    {
        throw std::runtime_error("not exist or is not directory");
    }
    std::vector<std::filesystem::path> path;
    for (const auto & p : std::filesystem::directory_iterator(input))
    {
        if(std::filesystem::is_regular_file(p.path())){
            path.push_back(p.path());
        }
        else{
            std::cout << "failed: " << p.path() << std::endl;
        }
    }

    return path;
}

void Imageprocess::process(const std::vector<std::filesystem::path> &imagepath, const std::filesystem::path &output){
    if(imagepath.empty()){
        throw std::runtime_error("empty");
    }
    std::filesystem::create_directories(output);
    int i = 0;
    for (const auto &p : imagepath){
        cv::Mat img = cv::imread(p.string());
        if(img.empty()){
            std::cout << "failed to open img: " << p << std::endl;
            continue;
        }
        cv::Mat img_resize, img_rgb;
        cv::resize(img, img_resize, cv::Size(width, height));
        cv::cvtColor(img_resize, img_rgb, cv::COLOR_BGR2RGB);
        auto f = std::to_string(i) + ".jpg";
        if(!cv::imwrite((output / f).string(), img_resize)){
            throw std::runtime_error("failed to save" + (output / f).string()) ;
        }
        else{
            std::cout << "save success: " << (output / f).string() << std::endl;
        }
        i++;
        cv::Mat img_nor;
        img_rgb.convertTo(img_nor, CV_32F, 1.0 / 255.0);
        
    }
}