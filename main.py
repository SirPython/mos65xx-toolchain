"""
http://archive.6502.org/datasheets/mos_6500_mpu_mar_1980.pdf
http://archive.6502.org/datasheets/mos_6500_mpu_nov_1985.pdf
http://pdf.datasheetcatalog.com/datasheet/UMC/mXyztwtz.pdf
"""
import os
import ctypes

import instruction_set

# https://stackoverflow.com/questions/142812/does-python-have-a-bitfield-type
class StatusRegister_bits(ctypes.LittleEndianStructure):
    _fields_ = [
            ("carry", ctypes.c_uint8, 1),
            ("zero", ctypes.c_uint8, 1),
            ("irq_disable", ctypes.c_uint8, 1),
            ("decimal_mode", ctypes.c_uint8, 1),
            ("brk_command", ctypes.c_uint8, 1),
            ("_", ctypes.c_uint8, 1),
            ("overflow", ctypes.c_uint8, 1),
            ("negative", ctypes.c_uint8, 1)
        ]

class StatusRegister(ctypes.Union):
    _fields_ = [("b", StatusRegister_bits),
                ("asbyte", ctypes.c_uint8)]

class MOS6500():
    def __init__(self):
        self.ram = [0] * 8192

        self.accumulator = 0
        self.index_x = 0
        self.index_y = 0
        self.program_counter = 0
        self.stack_pointer = 0
        self.status = StatusRegister()

        self.instruction_set = [0] * 0xFF
        self.instruction_set[0x69] = ADC_IMMEDIATE
        self.instruction_set[0x6D] = ADC_ABSOLUTE
        self.instruction_set[0x65] = ADC_ZEROPAGE
        self.instruction_set[0x61] = ADC_INDIRECTX
        self.instruction_set[0x71] = ADC_INDIRECTY
        self.instruction_set[0x75] = ADC_ZEROPAGEX
        self.instruction_set[0x7D] = ADC_ABSOLUTEX
        self.instruction_set[0x79] = ADC_ABSOLUTEY
        self.instruction_set[0x29] = AND_IMMEDIATE
        self.instruction_set[0x2D] = AND_ABSOLUTE
        self.instruction_set[0x25] = AND_ZEROPAGE
        self.instruction_set[0x21] = AND_INDIRECTX
        self.instruction_set[0x31] = AND_INDIRECTY
        self.instruction_set[0x35] = AND_ZEROPAGEX
        self.instruction_set[0x3D] = AND_ABSOLUTEX
        self.instruction_set[0x39] = AND_ABSOLUTEY
        self.instruction_set[0x0E] = ASL_ABSOLUTE
        self.instruction_set[0x06] = ASL_ZEROPAGE
        self.instruction_set[0x0A] = ASL_ACCUMULATOR
        self.instruction_set[0x16] = ASL_ZEROPAGEX
        self.instruction_set[0x1E] = ASL_ABSOLUTEX
        self.instruction_set[0x90] = BCC_RELATIVE
        self.instruction_set[0xB0] = BCS_RELATIVE
        self.instruction_set[0xF0] = BEQ_RELATIVE
        self.instruction_set[0x2C] = BIT_ABSOLUTE
        self.instruction_set[0x24] = BIT_ZEROPAGE
        self.instruction_set[0x30] = BMI_RELATIVE
        self.instruction_set[0xD0] = BNE_RELATIVE
        self.instruction_set[0x10] = BPL_RELATIVE
        self.instruction_set[0x00] = BRK_IMPLIED
        self.instruction_set[0x50] = BVC_RELATIVE
        self.instruction_set[0x70] = BVS_RELATIVE
        self.instruction_set[0x18] = CLC_IMPLIED
        self.instruction_set[0xD8] = CLD_IMPLIED
        self.instruction_set[0x58] = CLI_IMPLIED
        self.instruction_set[0xB8] = CLV_IMPLIED
        self.instruction_set[0x00] = NONE
        self.instruction_set[0x00] = NONE
        self.instruction_set[0x00] = NONE

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
        data = self.read_bytes(instruction.num_bytes - 1)

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

                # Check the registers and update flags. Some instructions
                # will update flags on their own if the accumulator is
                # unaffected.
                # Maybe check before and after to see which register is modified
                # ... could even do the same with the whole state. How about this:
                # the set_item can set a flag for which thing was modified,
                # and then this can check that flag and update the status.
                # or maybe the set_item goes directly to the routine to update
                # status
                self.update_flags()

    def __getitem__(self, k):
        if k == "a":
            return self.accumulator
        elif k == "x":
            return self.index_x
        elif k == "y":
            return self.index_y
        elif k == "pc":
            return self.program_counter
        elif k == "s":
            return self.stack_pointer
        elif k == "carry":
            return self.status.b.carry
        elif k == "zero":
            return self.status.b.zero
        elif k == "irq_disable":
            return self.status.b.irq_disable
        elif k == "decimal_mode":
            return self.status.b.decimal_mode
        elif k == "brk_command":
            return self.status.b.brk_command
        elif k == "overflow":
            return self.status.b.overflow
        elif k == "negative":
            return self.status.b.negative
        elif k == "status":
            return self.status.asbyte
        else:
            return self.ram[k]

    # So accumulator instructions can be passed "a"
    def __setitem__(self, k, v):
        if k == "a":
            self.accumulator = v
        elif k == "x":
            self.index_x = v
        elif k == "y":
            self.index_y = v
        elif k == "pc":
            self.program_counter = v
        elif k == "s":
            self.stack_pointer = v
        elif k == "carry":
            self.status.b.carry = v
        elif k == "zero":
            self.status.b.zero = v
        elif k == "irq_disable":
            self.status.b.irq_disable = v
        elif k == "decimal_mode":
            self.status.b.decimal_mode = v
        elif k == "brk_command":
            self.status.b.brk_command = v
        elif k == "overflow":
            self.status.b.overflow = v
        elif k == "negative":
            self.status.b.negative = v
        elif k == "status":
            self.status.asbyte = v
        else:
            self.ram[k] = v

    def __str__(self):
        ret = f"""Accumulator: {self.accumulator}
Index X: {self.index_x}
Index Y: {self.index_y}
Program Counter: {self.program_counter}
Stack Pointer: {self.stack_pointer}

Status.Carry: {self["carry"]}
Status.Zero: {self["zero"]}
Status.IRQDisable: {self["irq_disable"]}
Status.DecimalMode: {self["decimal_mode"]}
Status.BRKCommand: {self["brk_command"]}
Status.Overflow: {self["overflow"]}
Status.Negative: {self["negative"]}
"""


if __name__ == "__main__":
    with open(self.argv[1], "rb") as f:
        rom = f.read()

    mos = MOS6500()

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(mos)

        while True:
            ram_addr = input()

            if ram_addr == "":
                break
            else:
                ram_addr = int(ram_addr)
                print(f"RAM[{ram_addr}]: {mos.ram[ram_addr]}")

        mos.exec(1)