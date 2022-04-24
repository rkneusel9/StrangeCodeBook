#include <stdio.h>

typedef union {
    float f;
    unsigned int d;
} fp_t;

int main(int argc, char *argv[]) {
    fp_t fp;

    //  Assign a float
    fp.f = 3.14159265;

    //  Print the hex
    printf("%0.8f in hex is %08x\n", fp.f, fp.d);

    return 0;
}

