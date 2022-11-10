#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <vector>
#include <numeric>
#include <iterator>
#include <algorithm>
#include <chrono> //NOLINT (build/c++11)
using namespace std;


class Book {
public:
    int ISBN;
    string language, type;
    Book(string line){
        stringstream ss(line);
        int count = 0;
        while(ss.good()){
            string substr;
            getline(ss,substr,',');
            if (count == 0){
                //assign ISBN
                ISBN = stoi(substr);
            }
            if (count == 1){
                language = substr;
            }
            if (count == 2){
                type = substr;
            }
            count++;
        }
    }
};

int linearSearch(vector <Book> newbook, vector <Book> request){
    vector<Book>::iterator ptr;
    vector<Book>::iterator ptr2;
    int match = 0;

    for(ptr = request.begin(); ptr <= request.end();ptr++){
        for(ptr2 = newbook.begin(); ptr2 <= newbook.end(); ptr2++){
            if(ptr->ISBN == ptr2->ISBN && ptr->language == ptr2->language && ptr->type == ptr2->type){
                match++;
            }
        }
    }
    return match;
}

bool compareForSort(const Book& n1, const Book& n2){
    //cout << n1.ISBN << "\t" << n2.ISBN << "\n";
    if(n1.ISBN == n2.ISBN){
        if((n1.type).length() == (n2.type).length()){
            return n1.language > n2.language;
        }
        return (n1.type).length() < (n2.type).length();
    }
    return n1.ISBN > n2.ISBN;
}


int binarySearch(vector <Book> newbook,  vector <Book> request){
    vector<Book>::iterator ptr5;
    int match = 0;
    for(ptr5 = request.begin();ptr5<request.end();ptr5++){
    	vector<Book>::iterator ptr3 = newbook.begin();
    	vector<Book>::iterator ptr4 = prev(newbook.end(),1);
    	vector<Book>::iterator mid = ptr3;
    	int n = newbook.size();
	mid = next(mid, n/2);
    	//cout << ptr3->ISBN << "\t" << ptr4->ISBN << "\t" <<mid->ISBN << "\n";
        while((ptr3->ISBN > ptr4->ISBN) && (n>0)){	
    	    //cout << ptr3->ISBN << "\t" << ptr4->ISBN << "\t" <<mid->ISBN << "\t" << ptr5->ISBN << "\t" << n << "\n";
            if (ptr5->ISBN < mid->ISBN){
                ptr3 = next(mid, 1);
                n = n/2;
                mid = next(mid, n);
            }
            else{
                ptr4 = mid;
                n = n/2;
                mid = prev(mid, n);
            }   
        }
        if((mid->ISBN == ptr5->ISBN) && (mid->type == ptr5->type) &&(mid->language == ptr5->language)){
			match++;
	}

    }
    return match;
    
}

vector <Book> dataIntoVector(string filename){
    ifstream file;
    file.open(filename, ios::in);
    if(!file.is_open()){
        cout << "Error: cannot open file " << filename << "\n";
        exit(1); 
    }
    vector <Book> vec;

    string line;
    while(1){
        file >> line;
        if(file.eof()){
            break;
        }
        Book book = Book(line);
        vec.push_back(book);
    }
    file.close();
    return vec;
}


int main(int argc, char *argv[]) {
    int match = 0;

    if (argc < 3){
        cout << "./SearchNewBooks <newBooks.dat> <request.dat> <result_file.dat>\n";
        return -1;
    }

    char choice;
    double elapsed_us;
    ofstream myfile(argv[3], ios::out);
    std::chrono::high_resolution_clock::time_point start;
    std::chrono::high_resolution_clock::time_point end;
    vector <Book> newbooks = dataIntoVector(argv[1]);
    vector <Book> requests = dataIntoVector(argv[2]);
    while(1){   
        cout << "Choice of search method ([l]inear, [b]inary)?\n";
        cin >> choice;

            //ct.Reset()    
        switch(choice){
            case 'l':
                start = std::chrono::high_resolution_clock::now();
                match = linearSearch(newbooks, requests);
                end = std::chrono::high_resolution_clock::now();
                elapsed_us = std::chrono::duration<double, std::micro>(end-start).count();
                cout << "CPU time: " << elapsed_us << " microseconds\n";
                if(myfile.is_open()){
                    myfile << match << "\n";
                    myfile.close(); 
                }
                return 0;
            case 'b':       
                sort(newbooks.begin(), newbooks.end(), compareForSort); 
                start = std::chrono::high_resolution_clock::now();
                match = binarySearch(newbooks, requests);
                end = std::chrono::high_resolution_clock::now();
                elapsed_us = std::chrono::duration<double, std::micro>(end-start).count();
                cout << "CPU time: " << elapsed_us << " microseconds\n";
                if(myfile.is_open()){
                    myfile << match << "\n";
                    myfile.close(); 
                }
                return 0;
            default:
                cout << "Incorrect Choice\n";
                break;
        }
    }
}    
    
