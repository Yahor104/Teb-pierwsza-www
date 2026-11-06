#include <iostream>
using namespace std;

class Matemat {
public:
    float add(float a, float b) {
        return a + b;
    }
    float eXTRACT(float a, float b) {
        return a - b;
    }
    float division(float a, float b) {
        if (b == 0) {
            cout << "Nie zoąna dzelić przez 0!";
            return 0;
        }
        return a / b;
    }
    float multiplication(float a, float b) {
        return a * b;
    }
    int modulo(int a, int b) {
        return a % b;
    }
    int factorial(int a) {
        int wynik = 1;
        for (int i = 1; i <= a; i++) {
            wynik = wynik * i;
        }
        return wynik;
    }
    float square(float a) {
        return a * a;
    }
    float rectangle(float a, float b) {
        return a * b;
    }
    float kolo(float a) {
        float const P = 3.141592653589793238462643383279502884197169399375;
        return P * (a * a);
    }
};

int main() {
    Matemat m;
    int input;
    float input1;
    float input2;
    cout << "Wybierz działanie" << endl << "1.(dodawanie)" << endl << "2.(odejmowanie)" << endl << "3.(mnożenie)" << endl << "4.(dzielenie)" << endl << "5.(modulo)" << endl << "6.(factorial)" << endl << "7.(pole kwadratu)" << endl << "8.(pole prostakąta)" << endl << "9.(pole koła)" << endl;
    cin >> input;
    switch (input) {
        case 1:
            cout << "Dodawanie" << endl;
            cout << "Wpisz 1 liczbę: ";
            cin >> input1;
            cout << "Wpisz 2 liczbę: ";
            cin >> input2;
            cout << m.add(input1, input2) << endl;
            break;
        case 2:
            cout << "Odejmowanie" << endl;
            cout << "Wpisz 1 liczbę: ";
            cin >> input1;
            cout << "Wpisz 2 liczbę: ";
            cin >> input2;
            cout << m.eXTRACT(input1, input2) << endl;
            break;
        case 3:
            cout << "Mnożenie" << endl;
            cout << "Wpisz 1 liczbę: ";
            cin >> input1;
            cout << "Wpisz 2 liczbę: ";
            cin >> input2;
            cout << m.multiplication(input1, input2) << endl;
            break;
        case 4:
            cout << "dzielenie" << endl;
            cout << "Wpisz 1 liczbę: ";
            cin >> input1;
            cout << "Wpisz 2 liczbę: ";
            cin >> input2;
            cout << m.division(input1, input2) << endl;
            break;
        case 5:
            cout << "Modulo" << endl;
            cout << "Wpisz 1 liczbę: ";
            cin >> input1;
            cout << "Wpisz 2 liczbę: ";
            cin >> input2;
            cout << m.modulo(input1, input2) << endl;
            break;
        case 6:
            cout << "Factorial" << endl;
            cout << "Wpisz liczbę: ";
            cin >> input1;
            cout << m.factorial(input1) << endl;
            break;
        case 7:
            cout << "Pole kwadratu" << endl;
            cout << "Wpisz długość boka: ";
            cin >> input1;
            cout << m.square(input1) << endl;
            break;
        case 8:
            cout << "Pole prostokąta" << endl;
            cout << "Wpisz długość 1 boka: ";
            cin >> input1;
            cout << "Wpisz długość 2 boka: ";
            cin >> input2;
            cout << m.rectangle(input1, input2) << endl;
            break;
        case 9:
            cout << "Pole koła" << endl;
            cout << "Wpisz promień koła: ";
            cin >> input1;
            cout << m.kolo(input1) << endl;
            break;
        default:
            cout << "Niepoprawny wybór" << endl;
    }
    return 0;
}
