void adc_immediate(char *data, struct mos6500 *mos) {
    mos->accumulator = mos->accumulator + data[0] + mos->status.carry;

    // todo conditionally set carry bit
}
void adc_absolute(char *data, struct mos6500 *mos) {
    mos->accumulator = mos->accumulator + mos->ram[(data[1] << 8) + data[0]];
}
void adc_zeropage(char *data, struct mos6500 *mos) {
    mos->accumulator = mos->accumulator + mos->ram[data[0]];
}

struct op instruction_set[0xFF * sizeof(struct op)]; // max # of instructions
instruction_set[0x69] = {&adc_immediate, 2, 2};
instruction_set[0x6D] = {&adc_absolute,  4, 3};
instruction_set[0x65] = {&adc_zeropage,  3, 2};