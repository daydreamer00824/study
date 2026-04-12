#pragma once
#include<filesystem>
#include<vector>

class Imageprocess{
    public:
        Imageprocess(int w, int h);
	std::vector<std::filesystem::path> image_path(const std::filesystem::path &input);
        void process(const std::vector<std::filesystem::path> &imagepath, const std::filesystem::path &output);

    private:
        int width;
        int height;
};
