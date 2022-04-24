//
//  file: correlation_test.c
//
//  Serial correlation test
//
//  RTK, 13-Oct-2017
//  Last update:  13-Oct-2017
//
///////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <inttypes.h>

double next(int typ, FILE *g) {
    uint8_t b8;
    uint32_t b32;
    uint64_t b64;
    double d;

    switch (typ) {
        case 0:
            if (fread((void*)&b8, sizeof(uint8_t), 1, g) == 0)
                return -1;
            return (double)b8/256.0;
            break;
        case 1:
            if (fread((void*)&b32, sizeof(uint32_t), 1, g) == 0)
                return -1;
            return (double)b32/4294967296.0;
            break;
        case 2:
            if (fread((void*)&b64, sizeof(uint64_t), 1, g) == 0)
                return -1;
            return (double)(b64>>32)/4294967296.0;
            break;
        case 3:
            if (fread((void*)&d, sizeof(double), 1, g) == 0)
                return -1;
            return d;
            break;
        default:
            break;
    }
    return -1;
}


double corr(int typ, FILE *g, int *n) {
    double c,ui,u0,u1;
    double sum=0,ssum=0,sprod=0;

    *n = 1;
    ui = next(typ,g);
    if (ui==-1) return -1;
    u0 = ui;
    sum = u0;
    ssum = u0*u0;

    while (1) {
        u1 = next(typ,g);
        if (u1==-1) break;
        sum += u1;
        ssum += u1*u1;
        sprod += u0*u1;
        u0 = u1;
        (*n)++;
    }
    sprod += u1*ui;

    return ((*n)*sprod - sum*sum) / ((*n)*ssum - sum*sum);
}


int main(int argc, char *argv[]) {
    FILE *g;
    int typ,n;
    double c,m,s;

    if (argc == 1) {
        printf("\ncorr_test 0|1|2|3 <source>\n\n");
        printf("  0|1|2|3  - 0=byte, 1=unsigned 32-bit, 2=unsigned 64-bit, 3=double\n");
        printf("  <source> - source binary file\n\n");
        return 0;
    }

    typ = atoi(argv[1]);
    g = fopen(argv[2],"r");

    c = corr(typ, g, &n);
    m = -1.0/(n-1.0);
    s = (1.0/(n-1.0))*sqrt(n*(n-3.0)/(n+1.0));

    printf("\ncorr = %0.5f (n=%d), expected 95%% CI=[%0.5f, %0.5f]", c, n, m-2*s, m+2*s);
    if ((c >= m-2*s) && (c <= m+2*s))
        printf(", test PASSED\n\n");
    else
        printf(", test FAILED\n\n");
    fclose(g);
}


