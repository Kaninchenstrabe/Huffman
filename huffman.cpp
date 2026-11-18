#include "huffman.h"
#include <iostream>
#include <fstream>
#include <cstdint>

Node::Node(const int node_value, const char node_data){
            value = node_value;
            data = node_data;
        }
        // set & get methods
        int Node::getValue() {
                return value;
            }
        char Node::getData() {
                return data;
            }
        Node* Node::getLeft() {
            return left;
            }
        Node* Node::getRight() {
            return right;
            }
        bool Node::setNext(Node* element) {
                next = element;
                return false;
            }
        Node* Node::getNext() {
                return next;
            }
        // other methods
        bool Node::update_value() {
            if (left != nullptr && right != nullptr) {
                value = left->value + right->value;
                return false;
            } else {
                return true;
            }
        }
        bool Node::adopt(Node* node, const char side) {
            switch (side) {
                case 'L':
                    left = node;
                    update_value();
                    return false;
                case 'R':
                    right = node;
                    update_value();
                    return false;
                default:
                    return true;
            }
        }
        Node::~Node() {
                delete left;
                delete right;
            }

        // set & get methods
        bool List::setFirst(Node* element) {
            first = element;
            return false;
            }
        Node* List::getFirst() {
            if (first!=nullptr) {
                return first;
                }
            }
        int List::getValue(int index) {
                Node* helping_hand=first;
                for (int i=0;i<index;i++) {
                    helping_hand=helping_hand->getNext();
                }
                return helping_hand->getValue();
                }

        char List::getData(int index) {
                Node* helping_hand=first;
                for (int i=0;i<index;i++) {
                    helping_hand=helping_hand->getNext();
                }
                return helping_hand->getData();
                }
        bool List::append(Node* element) {
            if (element == nullptr) return true;
            element->setNext(nullptr);
            if (first == nullptr) {
                first = element;
                last = element;
            }else {
                last->setNext(element);
                last = element;
            }
            return false;
        }
        void List::clear() {
            first = nullptr;
            last = nullptr;
        }
        void List::concat(List& other) {
            if (other.first == nullptr) return;
            if (first == nullptr) {
                first = other.first;
                last = other.last;
            }else{
                last->setNext(other.first);
                last = other.last;
                other.first = nullptr;
                other.last = nullptr;
            }

        }
        int List::length() {
            Node* helping_hand=first;
            int len=0;
            if (first!=nullptr && last!=nullptr) {
                len++;
                while (helping_hand->getNext()!=nullptr) {
                    len++;
                    helping_hand=helping_hand->getNext();
                }
            }
            return len;
        }
        bool List::load_file(int* values, int len) {
            for (int i = 0; i<len; i++) {
                if (*(values+i)>0) {
                    append(new Node(*(values+i),static_cast<char>(i)));
                }
            }
            return false;
        }
        bool List::print_list() {
                for (int i=0; i<length(); i++) {
                    std::cout << i;
                    std::cout << ". ";
                    std::cout << getData(i);
                    std::cout << ", ";
                    std::cout << getValue(i) << std::endl;
                }
                return false;
            }
        int List::radix() {
                for (int i=0; i<16; i++) {
                    List L_base;
                    List R_base;
                    Node* helping_hand = getFirst();
                    while (helping_hand != nullptr) {
                        Node* nextNode = helping_hand->getNext();
                        if (((helping_hand->getValue() >> i)&1)==0) {
                            L_base.append(helping_hand);
                        } else {
                            R_base.append(helping_hand);
                        }
                        helping_hand=nextNode;
                    }
                    clear();
                    concat(L_base);
                    concat(R_base);
                }
                return 0;
            }


        void H_tree::DFS(Node* root, uint32_t bits, uint8_t depth) {
        if (root == nullptr) return;
        if (root->getLeft() == nullptr && root ->getRight () == nullptr) {
            if (depth == 0) depth = 1;
            codebook[(unsigned char)root->getData()] = {bits, depth};
        }

        DFS(root->getLeft(), (bits << 1) | 0, depth+1);
        DFS(root->getRight(), (bits << 1) | 1, depth+1);
    }

        bool H_tree::load_file(std::string filename) {
            std::ifstream File;
            File.open(filename);
            std::string tekst;
            int occurences[256];
            for (int & occurence : occurences){
                occurence=0;
            }
            char field;
            while (getline(File, tekst)) {
                for (int i=0; i<tekst.length(); i++) {
                    occurences[static_cast<unsigned char>(tekst[i])]+=1;
                }
            }
            File.close();
            tree.load_file(&occurences[0], sizeof(occurences)/sizeof(occurences[0]));
            this->len = tree.length();
            return false;
            } // Load a file into a linked list
        bool H_tree::print_list() {
            tree.print_list();
            return false;
        }
        bool H_tree::Huffmanize() {
            for (int i=0; i<len-1; i++) {
                tree.radix();
                auto element = new Node(0,' ');
                element->adopt(tree.getFirst(), 'L');
                element->adopt(tree.getFirst()->getNext(), 'R');
                element->setNext(tree.getFirst()->getNext()->getNext());
                tree.setFirst(element);
            }
            return false;
        } // Turn a linked list into a Huffman (weighted) tree
        void H_tree::dictionarize() {
                for (auto & i : codebook) {
                    i = {.bits = 0,.length = 0};
                }
                DFS(tree.getFirst(),0,0);
            } // Create a dictionary character -> Huffman code
        void H_tree::print_dictionary() {
            for (int i=0; i<256; i++) {
                if (codebook[i].length>0) {
                    std::cout << static_cast<char>(i) << "->";
                    for (int b = codebook[i].length -1; b>=0; b--) {
                        std::cout << ((codebook[i].bits >> b) & 1);
                    }
                    std::cout << std::endl;
                }
            }
        }
        int H_tree::encode(const char* input, int input_len, char* out_bits) {
                int out_pos = 0;
                for (int i = 0; i < input_len; i++) {
                    HuffCode code = codebook[static_cast<unsigned char>(input[i])];
                    for (int b = code.length - 1; b >= 0; b--) {
                        out_bits[out_pos++] = ((code.bits >> b) & 1) ? '1' : '0';
                    }
                }
                out_bits[out_pos] = '\0';
                return out_pos;
            }
        char* H_tree::decode(char* bitstream) {
            char* i = bitstream;
            int n = 0 ;
            Node* helper = tree.getFirst();
            if (helper == nullptr) return bitstream;

            while (*i != '\0') {
                if (*i == '0') {
                    helper = helper->getLeft();
                } else if (*i == '1') {
                    helper = helper->getRight();
                }
                if (helper == nullptr) {
                    // Błąd w strumieniu bitów lub drzewo ma 1 węzeł
                    break;
                }
                if (helper != nullptr && helper->getLeft() == nullptr && helper->getRight() == nullptr) {
                    bitstream[n++] = helper->getData();
                    helper = tree.getFirst();
                }
                i++;
            }
            bitstream[n] = '\0'; // Terminate the decoded string so leftover bits aren't printed
            return bitstream;
        }
        bool H_tree::prepare(std::string filename) {
            load_file(filename);
            Huffmanize();
            dictionarize();
            return false;
        }
