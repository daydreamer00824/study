#include <iostream>
#include <fstream>

int main() {
    std::ifstream infile("number.txt");

    int i = 0;

    if (!infile) {
        std::cout << "empty" << '\n';
        return 1;
    }
    int sum = 0;
    while (infile >> i) {
        std::cout << "file is :" << i << std::endl;
        sum += i;
    }

    infile.close();

    std::ofstream outfile("result.txt");

    if (!outfile) {
        return 1;
    }
    

    outfile << sum << '\n';

    outfile.close();


    return 0;
}