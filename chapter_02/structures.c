#include <string.h>
#include <stdlib.h>
#include <stdio.h>

typedef char string[32];

typedef struct {
    int area, exchange, number;
} phone_number_t;

typedef struct {
    int month, day, year;
} birthday_t;

typedef struct {
    string first, last;
    string address;
    phone_number_t phone;
    birthday_t bday;
} person_t;

int main(int argc, char *argv[]) {
    person_t person; // static declaration
    person_t *p;
    FILE *f;

    //  fill in the structure
    strcpy(person.first, "Winston");
    strcpy(person.last, "Rothschild");
    strcpy(person.address, "451 Fire St");
    person.phone.area = 219;
    person.phone.exchange = 555;
    person.phone.number = 1234;
    person.bday.year = 1974;
    person.bday.month = 3;
    person.bday.day = 9;

    //  print something
    printf("birthday: %02d/%02d/%4d, ", person.bday.month,
        person.bday.day, person.bday.year);
    printf("phone: %03d-%03d-%04d, ", person.phone.area,
        person.phone.exchange, person.phone.number);
    printf("address: %s, ", person.address);
    printf("name: %s %s\n", person.first, person.last);

    //  heap instance
    p = (person_t *)malloc(sizeof(person_t));

    strcpy(p->first, "Dalton");
    strcpy(p->last, "Humphrey");
    strcpy(p->address, "42 Deep Thought Ln");
    p->phone.area = 912;
    p->phone.exchange = 555;
    p->phone.number = 4321;
    p->bday.year = 1955;
    p->bday.month = 9;
    p->bday.day = 2;

    //  print something
    printf("birthday: %02d/%02d/%4d, ", p->bday.month,
        p->bday.day, p->bday.year);
    printf("phone: %03d-%03d-%04d, ", p->phone.area,
        p->phone.exchange, p->phone.number);
    printf("address: %s, ", p->address);
    printf("name: %s %s\n", p->first, p->last);

    //  dump on disk
    f = fopen("dalton", "wb");
    fwrite((void *)p, sizeof(person_t), 1, f);
    fclose(f);

    free(p);

    return 0;
}

