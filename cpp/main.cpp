#include <iostream>
#include <string>
#include <vector>
#include <sstream>

std::vector<int> means(std::string &getlines) {
    std::vector<int> shu;
    shu.reserve(5);
    std::istringstream ss(getlines);
    int s;
    if(getlines.empty()){
        std::cout << "empty!!" << '\n';
        return shu;
    }
    while (ss >> s) {
        shu.push_back(s);
    }
    return shu;
}

int main() {
    std::string lines;
    getline(std::cin, lines);

    std::vector<int> s = means(lines);
    int shu = 0;
    for (auto &p : s) {
        shu += p;
        std::cout << p << std::endl;
    }
    std::cout << shu / s.size() << std::endl;

    return 0;
}
