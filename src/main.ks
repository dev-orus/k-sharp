#include <stdio.h>

class Test {
    int x = 10;
    int y = 190;
    int __init__(this) {
        this.x = 0x1903;
    }
}

int main() {
    int* ptr = 10;
    Test mytest;
    printf("{0}, {1}", mytest.x, mytest.y);
}