#include <iostream>


class Node {
private:
    int value;
    Node* left;
    Node* right;
public:
    Node(const int node_value){
        value = node_value;
        left = nullptr;
        right = nullptr;
    }
    bool update_value() {
        if (left != nullptr && right != nullptr) {
            return true;
        } else {
            value = left->value + right->value;
            return false;
        }
    }
    bool adopt(Node* node, const char side) {
        switch (side) {
            case 'L':
                left = node;
                return false;
            case 'R':
                right = node;
                return false;
            default:
                return true;
        }
    }
};
class Element {
    private:
        int value=0;
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
            value = el_value;
             return false;
        }
        int getValue() {
            return value;
        }

};
class List {
    private:
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
        Element* getFirst() {
            return first;
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

};
class Sort {
    private:
        int r = 1;
        int len = 0;
        List list;
        Element hand = Element();
    public:
        bool setLen(int value) {
            len = value;
            return false;
        }
        bool load_list(int* data) {
            for (int i=0; i<len; i++) {
                auto* element = new Element();
                element->setValue(*(data+i));
                if (i == 0) {
                    list.insert(element);
                } else if (i>0) {
                    list.append(element);
                }

            }
            return false;
        }
        bool print_list() {
            for (int i=0; i<len; i++) {
                std::cout << list.getValue(i) << std::endl;
            }
            return false;
        }
        int radix() {



            for (int i=0; i<5; i++) {
                List L_base;
                List R_base;
                Element* helping_hand = list.getFirst();
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
                list.clear();
                list.concat(L_base);
                list.concat(R_base);

            }
            return 0;
        }
};

class Huffman {
    private:
    public:


};
using namespace std;



int main() {
    int list[6] = {7, 2, 5, 1, 4, 3};
    Sort algo;
    std::cout << "done" << std::endl;
    algo.setLen(sizeof(list)/sizeof(int));
    std::cout << "done" << std::endl;
    algo.load_list(&list[0]);
    std::cout << "done" << std::endl;
    algo.print_list();
    std::cout << "done" << std::endl;
    algo.radix();
    std::cout << "done" << std::endl;
    algo.print_list();

    return 0;
}