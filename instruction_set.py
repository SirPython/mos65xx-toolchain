ADC_IMMEDIATE = Instruction(
    lambda data, mos: data,
    2,2
)
ADC_ABSOLUTE = Instruction(
    lambda data, mos: data,
    4,3
)
ADC_ZEROPAGE = Instruction(
    lambda data, mos: data,
    3,2
)