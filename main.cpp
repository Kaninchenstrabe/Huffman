#include <cmath>
#include <iostream>


class Node {
    protected:
        int value;
        char data;
        Node* left;
        Node* right;
    public:
        Node(const int node_value, const char node_data){
            value = node_value;
            data = node_data;
            left = nullptr;
            right = nullptr;
        }
        bool update_value() {
            if (left != nullptr && right != nullptr) {
                value = left->value + right->value;
                return false;
            } else {
                return true;;
            }
        }
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
        Node* getLeft() {
            return left;
        }
        Node* getRight() {
            return right;
        }
};
class Element {
    protected:
        Node el_node = Node(0,' ');
        Element* next = nullptr;
    public:
         bool setNext(Element* element) {
            next = element;
            return false;
        }
        Element* getNext() {
            return next;
        }
        bool setValue(int el_value) {
            el_node.setValue(el_value);
             return false;
        }
        int getValue() {
            return el_node.getValue();
        }
        bool setData(char Data) {
             el_node.setData(Data);
             return false;
         }
        char getData() {
             return el_node.getData();
         }
        Node* getAddress() {
             return &el_node;
         }
        bool setNode(Node* node) {
             el_node=*node;
             return false;
         }

};
class List {
    protected:
        Element* last=nullptr;
        Element* first=nullptr;
        Element* helping_hand=nullptr;
    public:

        bool insert(Element* element) {
            if (first != nullptr) {
                element->setNext(first->getNext());
            }
            first = element;
            if (last == nullptr) {
                last = element;
            }
            return false;
        }
        bool append(Element* element) {
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
        Element* getAddress(int index) {
            helping_hand=first;
            for (int i=0;i<index;i++) {
                helping_hand=helping_hand->getNext();
            }
            return helping_hand;
        }
        Element* getFirst() {
            return first;
        }
        bool setFirst(Element* element) {
            first = element;
            return false;
        }
        Element* getLast() {
            return last;
        }
        void clear() {
            first = nullptr;
            last = nullptr;
        }
        void setBounds(Element* newFirst, Element* newLast) {
            first = newFirst;
            last = newLast;
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
        bool load_list(int* values, char* data) {
            for (int i=0; i<length(); i++) {
                auto* element = new Element();
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

    public:
        bool load_list(int* values, char* data, int len) {

            for (int i=0; i<len; i++) {
                auto* element = new Element();
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
                Element* helping_hand = tree.getFirst();
                //i = i << 1;
                while (helping_hand != nullptr) {
                    Element* nextNode = helping_hand->getNext();

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
            //int i=0;
            int len = tree.length();
            for (int i=0; i<len-1; i++) {
                radix();
                auto element = new Element;
                Node *helper = element->getAddress();
                helper->adopt(tree.getFirst()->getAddress(), 'L');
                helper->adopt(tree.getFirst()->getNext()->getAddress(), 'R');
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
        char read(int directions) {
            Element* reader = tree.getFirst();
            int order = 0;

            for (int i=bitlength(directions); i>0; i--) {
                order = ((directions&((directions>>(i-1))<<2))>>2)%2;
                std::cout<<order<<std::endl;;
                //directions = directions >> 1;
                    if (order == 1){
                        reader->setNode(reader->getAddress()->getRight());
                    } else if (order == 0){
                        reader->setNode(reader->getAddress()->getLeft());
                    }
            }
            return reader->getAddress()->getData();
        }



};
using namespace std;

int bitlength(int num) {
    unsigned bits, var = (num < 0) ? -num : num;
    for(bits = 0; var != 0; ++bits) var >>= 1;
    return bits;
}
int main() {
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
    std::cout << algo.read(63);
    return 0;
}