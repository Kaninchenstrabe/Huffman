//
// Created by pawel on 18.11.2026.
//
#ifndef HUFFMAN_HUFFMAN_H
#define HUFFMAN_HUFFMAN_H

#include <cstdint>
#include <string>

class Node {
private:
    int value;
    char data;
    Node* left = nullptr;
    Node* right = nullptr;
    Node* next=nullptr;
public:
    Node(int node_value, char node_data);

    int getValue();

    char getData();

    Node *getLeft();

    Node *getRight();

    bool setNext(Node *element);

    Node *getNext();

    bool update_value();

    bool adopt(Node *node, char side);

    ~Node();
};
class List {
private:
    Node* last=nullptr;
    Node* first=nullptr;
public:
    bool setFirst(Node *element);

    Node *getFirst();

    int getValue(int index);

    char getData(int index);

    bool append(Node *element);

    void clear();

    void concat(List &other);

    int length();

    bool load_file(int *values, int len);

    bool print_list();

    int radix();
};
struct HuffCode {
    uint32_t bits = 0;
    uint8_t length =0;
};
class H_tree {
private:
    List tree;
    int len = 0;
    HuffCode codebook[256];
    void DFS(Node* root, uint32_t bits, uint8_t depth);
public:
    bool load_file(std::string filename);

    bool print_list();

    bool Huffmanize();

    void dictionarize();

    void print_dictionary();

    int encode(const char *input, int input_len, char *out_bits);

    char *decode(char *bitstream);

    bool prepare(std::string filename);
};
#endif //HUFFMAN_HUFFMAN_H
