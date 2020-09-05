import ctypes
from instruction_set import *

# https://problemkaputt.de/2k6specs.htm

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
    def __init__(self, ram):
        self.ram = [0] * ram

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
        self.instruction_set[0xC9] = CMP_IMMEDIATE
        self.instruction_set[0xCD] = CMP_ABSOLUTE
        self.instruction_set[0xC5] = CMP_ZEROPAGE
        self.instruction_set[0xC1] = CMP_INDIRECTX
        self.instruction_set[0xD1] = CMP_INDIRECTY
        self.instruction_set[0xD5] = CMP_ZEROPAGEX
        self.instruction_set[0xDD] = CMP_ABSOLUTEX
        self.instruction_set[0xD9] = CMP_ABSOLUTEY
        self.instruction_set[0xE0] = CPX_IMMEDIATE
        self.instruction_set[0xEC] = CPX_ABSOLUTE
        self.instruction_set[0xE4] = CPX_ZEROPAGE
        self.instruction_set[0xC0] = CPY_IMMEDIATE
        self.instruction_set[0xCC] = CPY_ABSOLUTE
        self.instruction_set[0xC4] = CPY_ZEROPAGE
        self.instruction_set[0xCE] = DEC_ABSOLUTE
        self.instruction_set[0xC6] = DEC_ZEROPAGE
        self.instruction_set[0xD6] = DEC_ZEROPAGEX
        self.instruction_set[0xDE] = DEC_ABSOLUTEX
        self.instruction_set[0xCA] = DEX_IMPLIED
        self.instruction_set[0x88] = DEY_IMPLIED
        self.instruction_set[0x49] = EOR_IMMEDIATE
        self.instruction_set[0x4D] = EOR_ABSOLUTE
        self.instruction_set[0x45] = EOR_ZEROPAGE
        self.instruction_set[0x41] = EOR_INDIRECTX
        self.instruction_set[0x51] = EOR_INDIRECTY
        self.instruction_set[0x55] = EOR_ZEROPAGEX
        self.instruction_set[0x5D] = EOR_ABSOLUTEX
        self.instruction_set[0x59] = EOR_ABSOLUTEY
        self.instruction_set[0xEE] = INC_ABSOLUTE
        self.instruction_set[0xE6] = INC_ZEROPAGE
        self.instruction_set[0xF6] = INC_ZEROPAGEX
        self.instruction_set[0xFE] = INC_ABSOLUTEX
        self.instruction_set[0xE8] = INX_IMPLIED
        self.instruction_set[0xC8] = INY_IMPLIED
        self.instruction_set[0x4C] = JMP_ABSOLUTE
        self.instruction_set[0x6C] = JMP_INDIRECT
        self.instruction_set[0x20] = JSR_ABSOLUTE
        self.instruction_set[0xA9] = LDA_IMMEDIATE
        self.instruction_set[0xAD] = LDA_ABSOLUTE
        self.instruction_set[0xA5] = LDA_ZEROPAGE
        self.instruction_set[0xA1] = LDA_INDIRECTX
        self.instruction_set[0xB1] = LDA_INDIRECTY
        self.instruction_set[0xB5] = LDA_ZEROPAGEX
        self.instruction_set[0xBD] = LDA_ABSOLUTEX
        self.instruction_set[0xB9] = LDA_ABSOLUTEY
        self.instruction_set[0xA2] = LDX_IMMEDIATE
        self.instruction_set[0xAE] = LDX_ABSOLUTE
        self.instruction_set[0xA6] = LDX_ZEROPAGE
        self.instruction_set[0xBE] = LDX_ABSOLUTEY
        self.instruction_set[0xB6] = LDX_ZEROPAGEY
        self.instruction_set[0xA0] = LDY_IMMEDIATE
        self.instruction_set[0xAC] = LDY_ABSOLUTE
        self.instruction_set[0xA4] = LDY_ZEROPAGE
        self.instruction_set[0xB4] = LDY_ZEROPAGEX
        self.instruction_set[0xBC] = LDY_ABSOLUTEX
        self.instruction_set[0x4E] = LSR_ABSOLUTE
        self.instruction_set[0x46] = LSR_ZEROPAGE
        self.instruction_set[0x4A] = LSR_ACCUMULATOR
        self.instruction_set[0x56] = LSR_ZEROPAGEX
        self.instruction_set[0x5E] = LSR_ABSOLUTEX
        self.instruction_set[0xEA] = NOP_IMPLIED
        self.instruction_set[0x09] = ORA_IMMEDIATE
        self.instruction_set[0x0D] = ORA_ABSOLUTE
        self.instruction_set[0x05] = ORA_ZEROPAGE
        self.instruction_set[0x01] = ORA_INDIRECTX
        self.instruction_set[0x11] = ORA_INDIRECTY
        self.instruction_set[0x15] = ORA_ZEROPAGEX
        self.instruction_set[0x1D] = ORA_ABSOLUTEX
        self.instruction_set[0x19] = ORA_ABSOLUTEY
        self.instruction_set[0x48] = PHA_IMPLIED
        self.instruction_set[0x08] = PHP_IMPLIED
        self.instruction_set[0x68] = PLA_IMPLIED
        self.instruction_set[0x28] = PLP_IMPLIED
        self.instruction_set[0x2E] = ROL_ABSOLUTE
        self.instruction_set[0x26] = ROL_ZEROPAGE
        self.instruction_set[0x2A] = ROL_ACCUMULATOR
        self.instruction_set[0x36] = ROL_ZEROPAGEX
        self.instruction_set[0x3E] = ROL_ABSOLUTEX
        self.instruction_set[0x6E] = ROR_ABSOLUTE
        self.instruction_set[0x66] = ROR_ZEROPAGE
        self.instruction_set[0x6A] = ROR_ACCUMULATOR
        self.instruction_set[0x76] = ROR_ZEROPAGEX
        self.instruction_set[0x7E] = ROR_ABSOLUTEX
        self.instruction_set[0x40] = RTI_IMPLIED
        self.instruction_set[0x60] = RTS_IMPLIED
        self.instruction_set[0xE9] = SBC_IMMEDIATE
        self.instruction_set[0xED] = SBC_ABSOLUTE
        self.instruction_set[0xE5] = SBC_ZEROPAGE
        self.instruction_set[0xE1] = SBC_INDIRECTX
        self.instruction_set[0xF1] = SBC_INDIRECTY
        self.instruction_set[0xF5] = SBC_ZEROPAGEX
        self.instruction_set[0xFD] = SBC_ABSOLUTEX
        self.instruction_set[0xF9] = SBC_ABSOLUTEY
        self.instruction_set[0x38] = SEC_IMPLIED
        self.instruction_set[0xF8] = SED_IMPLIED
        self.instruction_set[0x78] = SEI_IMPLIED
        self.instruction_set[0x8D] = STA_ABSOLUTE
        self.instruction_set[0x85] = STA_ZEROPAGE
        self.instruction_set[0x81] = STA_INDIRECTX
        self.instruction_set[0x91] = STA_INDIRECTY
        self.instruction_set[0x95] = STA_ZEROPAGEX
        self.instruction_set[0x9D] = STA_ABSOLUTEX
        self.instruction_set[0x99] = STA_ABSOLUTEY
        self.instruction_set[0x8E] = STX_ABSOLUTE
        self.instruction_set[0x86] = STX_ZEROPAGE
        self.instruction_set[0x96] = STX_ZEROPAGEY
        self.instruction_set[0x8C] = STY_ABSOLUTE
        self.instruction_set[0x84] = STY_ZEROPAGE
        self.instruction_set[0x94] = STY_ZEROPAGEX
        self.instruction_set[0xAA] = TAX_IMPLIED
        self.instruction_set[0xA8] = TAY_IMPLIED
        self.instruction_set[0xBA] = TSX_IMPLIED
        self.instruction_set[0x8A] = TXA_IMPLIED
        self.instruction_set[0x9A] = TXS_IMPLIED
        self.instruction_set[0x98] = TYA_IMPLIED

    def load(self, rom):
        self.rom = rom
        self.program_counter = 0
        self.ram = [0] * len(self.ram)

    def read_bytes(self, n=1):
        ret = []

        for i in range(n):
            ret.append(self.rom[self.program_counter])
            self.program_counter += 1

        return ret

    def read_instruction(self):
        """
        Raises KeyError when an invalid opcode is read.
        """
        opcode = self.read_bytes()[0]
        instruction = self.instruction_set[opcode]

        if instruction == 0:
            raise KeyError

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

    def update_flags(self):
        pass

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
        return f"""Accumulator: {self.accumulator}
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