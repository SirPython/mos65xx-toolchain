#ifndef MOS6500_H
#define MOS6500_H

struct {
    char ram[8192];

    char accumulator;
    char index_y;
    char index_x;
    short program_counter;
    short stack_pointer;
    struct {
        carry: 1;
        zero: 1;
        irq_disable: 1;
        decimal_mode: 1;
        brk_command: 1;
        _: 1;
        overflow: 1;
        negative: 1;
    } status;
} mos6500;


#endif /* end of include guard: MOS6500_H */