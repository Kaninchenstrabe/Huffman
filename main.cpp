#include <cstdint>
#include <iostream>
#include <fstream>

class Node {
    private:
        int value;
        char data;
        Node* left = nullptr;
        Node* right = nullptr;
        Node* next=nullptr;
    public:
        Node(const int node_value, const char node_data){
            value = node_value;
            data = node_data;
        }
        // set & get methods
        int getValue() {
                return value;
            }
        char getData() {
                return data;
            }
        Node* getLeft() {
            return left;
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
                return true;
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
        ~Node() {
                delete left;
                delete right;
            }
};

class List {
    private:
        Node* last=nullptr;
        Node* first=nullptr;
    public:
        // set & get methods
        bool setFirst(Node* element) {
            first = element;
            return false;
            }
        Node* getFirst() {
            if (first!=nullptr) {
                return first;
                }
            }
        int getValue(int index) {
                Node* helping_hand=first;
                for (int i=0;i<index;i++) {
                    helping_hand=helping_hand->getNext();
                }
                return helping_hand->getValue();
                }
        char getData(int index) {
                Node* helping_hand=first;
                for (int i=0;i<index;i++) {
                    helping_hand=helping_hand->getNext();
                }
                return helping_hand->getData();
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
        int length() {
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
        bool load_file(int* values, int len) {
            for (int i = 0; i<len; i++) {
                if (*(values+i)>0) {
                    append(new Node(*(values+i),static_cast<char>(i)));
                }
            }
            return false;
        }
        bool print_list() {
                for (int i=0; i<length(); i++) {
                    std::cout << i;
                    std::cout << ". ";
                    std::cout << getData(i);
                    std::cout << ", ";
                    std::cout << getValue(i) << std::endl;
                }
                return false;
            }
        int radix() {
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
};
struct HuffCode {
    uint32_t bits = 0;
    uint8_t length =0;
};
class H_tree {
    private:
        List tree;
        int len;
        HuffCode codebook[256];
        void DFS(Node* root, uint32_t bits, uint8_t depth) {
        if (root == nullptr) return;
        if (root->getLeft() == nullptr && root ->getRight () == nullptr) {
            if (depth == 0) depth = 1;
            codebook[(unsigned char)root->getData()] = {bits, depth};
        }

        DFS(root->getLeft(), (bits << 1) | 0, depth+1);
        DFS(root->getRight(), (bits << 1) | 1, depth+1);
    }
public:
        bool load_file(std::string filename) {
            std::ifstream File;
            File.open(filename);
            std::string tekst;
            int occurences[256];
            for (int i=0; i<256; i++){
                occurences[i]=0;
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
        bool print_list() {
            tree.print_list();
            return false;
        }
        bool Huffmanize() {
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
        void dictionarize() {
                for (auto & i : codebook) {
                    i = {.bits = 0,.length = 0};
                }
                DFS(tree.getFirst(),0,0);
            } // Create a dictionary character -> Huffman code
        void print_dictionary() {
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
        int encode(const char* input, int input_len, char* out_bits) {
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
        char* decode(char* bitstream) {
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
                if (helper != nullptr && helper->getLeft() == nullptr && helper->getRight() == nullptr) {
                    bitstream[n++] = helper->getData();
                    helper = tree.getFirst();
                }
                i++;
            }
            bitstream[n] = '\0'; // Terminate the decoded string so leftover bits aren't printed
            return bitstream;
        }
        bool prepare(std::string filename) {
            load_file(filename);
            Huffmanize();
            dictionarize();
            return false;
        }
};

int main() {
    H_tree algo;
    algo.prepare("script.txt");
    char text[] = "the queen bee is the queenest of all the queer little fuckers - bees\0";
    char encoded[256];
    std::cout << "Input text: " << text << std::endl;
    int total_bits = algo.encode(text, sizeof(text)/sizeof(text[0]), encoded);
    std::cout << "Compressed text to " << total_bits << " bits: \n"<< encoded <<  std::endl;
    std::cout << "Doing so allowed to save " << 8*sizeof(text)-total_bits << " bits (" <<
        100*(1 - static_cast<float>(total_bits) / (8 * static_cast<float>(sizeof(text)))) <<
            "% less)\nDecoding encoded bits...\nResults: ";

    std::cout << algo.decode(&encoded[0]);
    return 0;
}