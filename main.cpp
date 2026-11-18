
#include <iostream>
#include "huffman.h"

int main() {
    H_tree algo;
    algo.prepare("script.txt");
    char text[] = "test testuje testowany program, ktory pod wplywem testowany jest okmqav\0";
    char* encoded = new char[sizeof(text)/sizeof(text[0])*32+1];
    std::cout << "Input text: " << text << std::endl;
    int total_bits = algo.encode(text, sizeof(text)/sizeof(text[0]), encoded);
    std::cout << "Compressed text to " << total_bits << " bits: \n"<< encoded <<  std::endl;
    std::cout << "Doing so allowed to save "` << 8*sizeof(text)-total_bits << " bits (" <<
        100*(1 - static_cast<float>(total_bits) / (8 * static_cast<float>(sizeof(text)))) <<
            "% less)\nDecoding encoded bits...\nResults: ";

    std::cout << algo.decode(&encoded[0]);
    return 0;
}