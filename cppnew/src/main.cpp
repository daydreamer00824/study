#include<iostream>
#include<fstream>
#include<filesystem>
#include<string>
#include<vector>
#include<stdexcept>

std::vector<std::filesystem::path> filepath (const std::filesystem::path &path, const std::string &ext){
    if (!std::filesystem::exists(path) || !std::filesystem::is_directory(path))
    {
        throw std::runtime_error("输入目录不存在or输入路径不是目录");
    }

    std::vector<std::filesystem::path> images;

    for (const auto &f : std::filesystem::directory_iterator(path)){
        if(f.is_regular_file() && f.path().extension().string() == ext){
            images.push_back(f.path());
        }
    }

    return images;
}

void report(const std::filesystem::path &outfile, const std::vector<std::filesystem::path> &image){
    if (!std::filesystem::exists(outfile) || !std::filesystem::is_directory(outfile))
    {
        throw std::runtime_error("输出目录不存在或不是目录");
    }
    std::ofstream out(outfile / "report.txt", std::ios::app);
    if(!out.is_open()){
        throw std::runtime_error("无法打开输出文件");
    }
    for (const auto & file : image)
    {
        out << "file: " << file.filename().string()
            <<" | 文件名: " << file.stem().string()
            << " | 后缀" << file.extension().string() << std::endl;
    }
    out.close();   
}

int main(int argc, char *argv[]){
    if(argc < 4){
        std::cerr << "用法: ./app <input_dir> <output_dir> <extension>" << std::endl;
        return 1;
    }

    std::filesystem::path input = argv[1];
    std::filesystem::path output = argv[2];
    std::string ext = argv[3];
    std::vector<std::filesystem::path> files;

    try
    {
       files = filepath(input, ext);
       std::cout << "共找到 " << files.size() << " 个文件" << std::endl;
       report(output, files);
       std::cout << "报告生成成功: " << std::endl;
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
        return 1;
    }

    return 0;
}
