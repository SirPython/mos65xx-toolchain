void adc_immediate(char *data, struct mos6500 *mos) {

}

struct op instruction_set[0xFF * sizeof(struct op)]; // max # of instructions
instruction_set[0x69] = {&adc_immediate, 2, 2};