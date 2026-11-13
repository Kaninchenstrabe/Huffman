#include <cmath>
#include <iostream>


class Node {
    private:
        int value;
        char data;
        Node* left=nullptr;
        Node* right=nullptr;
        Node* next=nullptr;
    public:
        Node(const int node_value, const char node_data){
            value = node_value;
            data = node_data;
        }
        // set & get methods
        bool setValue(int node_value) {
                value = node_value;
                return false;
            }
        int getValue() {
                return value;
            }
        bool setData(int node_data) {
                data = node_data;
                return false;
            }
        char getData() {
                return data;
            }
        bool setLeft(Node* node) {
            left = node;
            return false;
            }
        Node* getLeft() {
            return left;
            }
        bool setRight(Node* node) {
            left = node;
            return false;
            }
        Node* getRight() {
            return right;
            }
        bool setNext(Node* element) {
                next = element;
                return false;
            }
        Node* getNext() {
                return next;
            }
        // other methods
        bool update_value() {
            if (left != nullptr && right != nullptr) {
                value = left->value + right->value;
                return false;
            } else {
                return true;;
            }
        }
        bool adopt(Node* node, const char side) {
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
        // destructor?
};

class List {
    private:
        Node* last=nullptr;
        Node* first=nullptr;
        Node* helping_hand=nullptr;
    public:
        // set & get methods
        bool setFirst(Node* element) {
            first = element;
            return false;
            }
        Node* getFirst() {
            return first;
            }
        Node* getLast() {
            return last;
            }
        int getValue(int index) {
                helping_hand=first;
                for (int i=0;i<index;i++) {
                    helping_hand=helping_hand->getNext();
                }
                return helping_hand->getValue();
                }
        char getData(int index) {
                helping_hand=first;
                for (int i=0;i<index;i++) {
                    helping_hand=helping_hand->getNext();
                }
                return helping_hand->getData();
                }
        // other
        bool insert(Node* element) {
            if (first != nullptr) {
                element->setNext(first->getNext());
            }
            first = element;
            if (last == nullptr) {
                last = element;
            }
            return false;
        }
        bool append(Node* element) {
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
        void clear() {
            first = nullptr;
            last = nullptr;
        }
        void concat(List& other) {
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
        // destructor?
        int length() {
            helping_hand=first;
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
        // OLD but ill probably need them later
        bool load_list(int* values, char* data) {
            for (int i=0; i<length(); i++) {
                auto* element = new Node(0,' ');
                element->setValue(*(values+i));
                element->setData(*(data+i));
                if (i == 0) {
                    insert(element);
                } else if (i>0) {
                    append(element);
                }

            }
            return false;
        }
        bool print_list() {
            for (int i=0; i<length(); i++) {
                std::cout << getData(i) << std::endl;
            }
            return false;
        }
};

class Huffman {
    private:
        List tree;
        // if huffman class will remain with only one variable and just a set of methods consider moving the methods to list
    public:
        bool load_list(int* values, char* data, int len) {

            for (int i=0; i<len; i++) {
                auto* element = new Node(0,' ');
                element->setValue(*(values+i));
                element->setData(*(data+i));
                if (i == 0) {
                    tree.insert(element);
                } else if (i>0) {
                    tree.append(element);
                }

            }
            return false;
        }
        bool print_list() {
            for (int i=0; i<tree.length(); i++) {
                std::cout << i;
                std::cout << ". ";
                std::cout << tree.getData(i);
                std::cout << ", ";
                std::cout << tree.getValue(i) << std::endl;
            }
            return false;
        }
        int radix() {
            for (int i=0; i<5; i++) {
                List L_base;
                List R_base;
                Node* helping_hand = tree.getFirst();
                while (helping_hand != nullptr) {
                    Node* nextNode = helping_hand->getNext();
                    if (((helping_hand->getValue() >> i)&1)==0) {
                        L_base.append(helping_hand);
                    } else {
                        R_base.append(helping_hand);
                    }
                    helping_hand=nextNode;
                }
                tree.clear();
                tree.concat(L_base);
                tree.concat(R_base);
            }
            return 0;
        }
        bool generate() {
            int len = tree.length();
            for (int i=0; i<len-1; i++) {
                radix();
                auto element = new Node(0,' ');
                element->adopt(tree.getFirst(), 'L');
                element->adopt(tree.getFirst()->getNext(), 'R');
                element->setNext(tree.getFirst()->getNext()->getNext());
                tree.setFirst(element);
            }
            return false;
        }
        int bitlength(int num) {
            unsigned bits, var = (num < 0) ? -num : num;
            for(bits = 0; var != 0; ++bits) var >>= 1;
            return bits;
        }
        // WIP
        char read(int directions) {
            Node* reader = tree.getFirst();
            int order = 0;
            for (int i=bitlength(directions); i>0; i--) {
                order = ((directions&((directions>>(i-1))<<2))>>2)%2;
                std::cout<<order<<std::endl;;
                //directions = directions >> 1;
                    if (order == 1){
                        reader=reader->getRight();
                    } else if (order == 0){
                        reader=reader->getLeft();
                    }
            }
            return reader->getData();
        }
};
using namespace std;

int main() {
    //CLEAN TS UP
    int list[] = {7, 2, 5, 1, 4, 3, 1, 6, 8};
    char data[] = {'a','b','c','d','e','f','g','h','i'};
    Huffman algo;
    std::cout << "done" << std::endl;
    std::cout << "done" << std::endl;
    algo.load_list(&list[0], &data[0], min(sizeof(list)/sizeof(list[0]), sizeof(data)/sizeof(data[0])));
    std::cout << "done" << std::endl;
    algo.print_list();
    std::cout << "done" << std::endl;
    //algo.radix();
    //std::cout << "done" << std::endl;
    //algo.print_list();
    std::cout << "done" << std::endl;
    algo.generate();
    std::cout << "done" << std::endl;
    algo.print_list();
    std::cout << algo.read(5);
    return 0;
}