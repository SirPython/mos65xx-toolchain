#include <stdio.h>

int main(int argc, char **argv) {
    if(argc < 2) {
        perror("You need to specify a ROM to run.");
        return 1;
    }
    rom = fopen(argv[1], "rb");

    struct mos6500 mos;
    extern struct op instruction_set[];

    char byte;
    while((byte = getc(rom)) != EOF) {
        struct op = instruction_set[byte];

        char data[op.num_bytes - 1];
        fgets(data, op.num_bytes - 1, rom);

        op.exec(data, &mos);
    }
}