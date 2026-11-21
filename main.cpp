
#include <iostream>
#include "huffman.h"

int main() {
    H_tree algo;
    algo.prepare("script.txt");
    algo.print_dictionary();
    char text[] = "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible.\0";
    char* encoded = new char[sizeof(text)/sizeof(text[0])*32+1];
    std::cout << "\nInput text: " << text << '\n' << "The text takes " << 8*sizeof(text) << " bits.\n" << std::endl;
    int total_bits = algo.encode(text, sizeof(text)/sizeof(text[0]), encoded);
    std::cout << "Compressed text to " << total_bits << " bits: \n"<< encoded <<  std::endl;
    std::cout << "\nDoing so allowed to save " << 8*sizeof(text)-total_bits << " bits (" <<
        100*(1 - static_cast<float>(total_bits) / (8 * static_cast<float>(sizeof(text)))) <<
            "% less)\n\nDecoding encoded bits...\nResults: ";

    std::cout << algo.decode(&encoded[0]);
    return 0;
}