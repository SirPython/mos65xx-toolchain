"""
http://archive.6502.org/datasheets/mos_6500_mpu_mar_1980.pdf
http://archive.6502.org/datasheets/mos_6500_mpu_nov_1985.pdf
http://pdf.datasheetcatalog.com/datasheet/UMC/mXyztwtz.pdf
"""

import instruction_set

class MOS6500():
    def __init__(self):
        self.ram = [0] * 8192

        self.accumulator = 0
        self.index_x = 0
        self.index_y = 0
        self.program_counter = 0
        self.stack_pointer = 0
        self.status = {
            "carry": 0,
            "zero": 0,
            "irq_disable": 0,
            "decimal_mode": 0,
            "brk_command": 0,
            "overflow": 0,
            "negative": 0
        }

        self.instruction_set = [0] * 0xFF
        self.instruction_set[0x69] = ADC_IMMEDIATE
        self.instruction_set[0x6D] = ADC_ABSOLUTE
        self.instruction_set[0x65] = ADC_ZEROPAGE

    def load(self, rom):
        self.rom = rom
        self.program_counter = 0
        self.ram = [0] * 8192

    def read_bytes(self, n=1):
        ret = []

        for i in range(n):
            ret.append(self.rom[self.program_counter])
            self.program_counter += 1

        return ret

    def read_instruction(self):
        instruction = self.instruction_set[self.read_bytes()]
        data = self.read_bytes(instruction.num_bytes)

        return instruction, data

    def exec(self, n=None):
        """
        Executes the program loaded with .load().

        n refers to the number of instructions to execute. If None, the entire
        program will be executed.
        """
        if n == None:
            pass
        else:
            for _ in range(n):
                instruction, data = self.read_instruction()
                instruction(data, self)


class Instruction():
    def __init__(self, fn, num_cycles, num_bytes):
        self.fn = fn
        self.num_cycles = num_cycles
        self.num_bytes = num_bytes

    def __call__(self, data, mos):
        self.fn()


if __name__ == "__main__":
    with open(self.argv[1], "rb") as f:
        rom = f.read()

    mos = MOS6500()

    while True:
        try:
            op =