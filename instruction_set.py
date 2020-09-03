# todo: figure out indirect y, figure out carry bits and overflow stuff
# todo: all instructions of same type have same # of bytes

class Instruction():
    def __init__(self, fn, num_cycles, num_bytes):
        self.fn = fn
        self.num_cycles = num_cycles
        self.num_bytes = num_bytes

    def mem_routine(addr, mos):
        """
        Some instructions modify the memory which with they interact. This
        function handles setting the memory value after the computations.
        """
        ret = self.fn(mos[addr], mos)

        if ret:
            mos[addr] = ret

class ImmediateInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2)

    def __call__(self, data, mos):
        self.fn(data[0], mos)
class AbsoluteInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 3)

    def __call__(self, data, mos):
        self.mem_routine(
            data[0] + (data[1] << 8),
            mos
        )
class ZeroPageInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2)

    def __call__(self, data, mos):
        self.mem_routine(data[0], mos)
class AccumulatorInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 1)

    def __call__(self, data, mos):
        self.fn("a", mos)
class ImpliedInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 1)

    def __call__(self, data, mos):
        self.fn(mos)
class IndirectXInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2)

    def __call__(self, data, mos):
        addr = data[0] + mos.index_x
        self.mem_routine(
            mos[addr] + (mos[addr + 1] << 8),
            mos
        )
class IndirectYInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2)

    def __call__(self, data, mos):
        self.mem_routine(
            mos[data[0]] + mos.index_y,
            mos
        )
class ZeroPageXInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2)

    def __call__(self, data, mos):
        self.mem_routine(data[0] + mos.index_x, mos)
class AbsoluteXInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 3)

    def __call__(self, data, mos):
        self.mem_routine(data[0] + data[1] + mos.index_x, mos)
class AbsoluteYInsturction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 3)

    def __call__(self, data, mos):
        self.mem_routine(data[0] + data[1] + mos.index_y, mos)
class RelativeInstruction(Instruction):
    def __init__(self, status_flag, cond_val, num_cycles, num_bytes):
        self.status_flag = status_flag
        self.cond_val = cond_val

        self.num_cycles = num_cycles
        self.num_bytes = 2

    def __call__(self, data, mos):
        if mos[self.status_flag] == self.cond_val:
            mos["pc"] = (mos["pc"] & 0xFF) + data
class IndirectInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 3)

    def __call__(self, data, mos):
        addr = data[0] + (data[1] << 8)
        mos.program_counter = mos[addr] + (mos[addr + 1] << 8)
class ZeroPageYInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2)

    def __call__(self, data, mos):
        self.mem_routine(data[0] + mos.index_y, mos)

def ADC(data, mos):
    mos["a"] += data
ADC_IMMEDIATE = ImmediateInstruction(ADC, 2)
ADC_ABSOLUTE  = AbsoluteInstruction (ADC, 4)
ADC_ZEROPAGE  = ZeroPageInstruction (ADC, 3)
ADC_INDIRECTX = IndirectXInstruction(ADC, 6)
ADC_INDIRECTY = IndirectYInstruction(ADC, 6)
ADC_ZEROPAGEX = ZeroPageXInstruction(ADC, 4)
ADC_ABSOLUTEX = AbsoluteXInstruction(ADC, 4)
ADC_ABSOLUTEY = AbsoluteYInsturction(ADC, 4)

def AND(data, mos):
    mos["a"] = mos["a"] & data
AND_IMMEDIATE = ImmediateInstruction(AND, 2)
AND_ABSOLUTE  = AbsoluteInstruction (AND, 4)
AND_ZEROPAGE  = ZeroPageInstruction (AND, 3)
AND_INDIRECTX = IndirectXInstruction(AND, 6)
AND_INDIRECTY = IndirectYInstruction(AND, 6)
AND_ZEROPAGEX = ZeroPageXInstruction(AND, 4)
AND_ABSOLUTEX = AbsoluteXInstruction(AND, 4)
AND_ABSOLUTEY = AbsoluteYInsturction(AND, 4)

def ASL(data, mos):
    mos[data] = (mos[data] << 1) & 0xFF
    mos["carry"] = mos[data] & 0x7F
ASL_ABSOLUTE    = AbsoluteInstruction   (ASL, 6)
ASL_ZEROPAGE    = ZeroPageInstruction   (ASL, 5)
ASL_ACCUMULATOR = AccumulatorInstruction(ASL, 2)
ASL_ZEROPAGEX   = ZeroPageXInstruction  (6, 2)
ASL_ABSOLUTEX   = AbsoluteXInstruction  (7, 3)

BCC_RELATIVE = RelativeInstruction("carry", 0, 2)
BCS_RELATIVE = RelativeInstruction("carry", 1, 2)
BEQ_RELATIVE = RelativeInstruction("zero",  1, 2)

def BIT(data, mos):
    res = (mos["a"] & data) << 6
    mos["overflow"] = res & 0x01
    mos["negative"] = res << 1
BIT_ABSOLUTE = AbsoluteInstruction(BIT, 4, 3)
BIT_ZEROPAGE = ZeroPageInstruction(BIT, 3, 2)

BMI_RELATIVE = RelativeInstruction("negative", 1, 2)
BNE_RELATIVE = RelativeInstruction("zero",     0, 2)
BPL_RELATIVE = RelativeInstruction("negative", 0, 2)

def BRK(data, mos):
    pass
BRK_IMPLIED = ImpliedInstruction(BRK, 7, 1)

BVC_RELATIVE = RelativeInstruction("overflow", 0, 2)
BVS_RELATIVE = RelativeInstruction("overflow", 1, 2)

def CLC(mos):
    mos["carry"] = 0
CLC_IMPLIED = ImpliedInstruction(CLC, 2)

def CLD(mos):
    mos["decimal_mode"] = 0
CLD_IMPLIED = ImpliedInstruction(CLD, 2)

def CLI(mos):
    mos["irq_disable"] = 0
CLI_IMPLIED = ImpliedInstruction(CLI, 2)

def CLV(mos):
    mos["overflow"] = 0
CLV_IMPLIED = ImpliedInstruction(CLV, 2)

def compare(data, reg):
    res = reg - data
    mos["negative"] = 1 if res < 0 else mos["negative"]
    mos["zero"] = 1 if res == 0 else mos["zero"]
    mos["carry"] = 14 # how do i do this... i'm not good with carry bits clearly

def CMP(data, mos):
    compare(data, mos["a"])
CMP_IMMEDIATE = ImmediateInstruction(CMP, 2)
CMP_ABSOLUTE  = AbsoluteInstruction (CMP, 4)
CMP_ZEROPAGE  = ZeroPageInstruction (CMP, 3)
CMP_INDIRECTX = IndirectXInstruction(CMP, 6)
CMP_INDIRECTY = IndirectYInstruction(CMP, 5)
CMP_ZEROPAGEX = ZeroPageXInstruction(CMP, 4)
CMP_ABSOLUTEX = AbsoluteXInstruction(CMP, 4)
CMP_ABSOLUTEY = AbsoluteXInstruction(CMP, 4)

def CPX(data, mos):
    compare(data, mos["x"])
CPX_IMMEDIATE = ImmediateInstruction(CPX, 2)
CPX_ABSOLUTE  = AbsoluteInstruction (CPX, 4)
CPX_ZEROPAGE  = ZeroPageInstruction (CPX, 3)


def CPY(data, mos):
    compare(data, mos["y"])
CPY_IMMEDIATE = ImmediateInstruction(CPY, 2)
CPY_ABSOLUTE  = AbsoluteInstruction (CPY, 4)
CPY_ZEROPAGE  = ZeroPageInstruction (CPY, 3)

def DEC(data, mos):
    return mos[data] - 1
DEC_ABSOLUTE  = AbsoluteInstruction (DEC, 6)
DEC_ZEROPAGE  = ZeroPageInstruction (DEC, 5)
DEC_ZEROPAGEX = ZeroPageXInstruction(DEC, 6)
DEC_ABSOLUTEX = AbsoluteXInstruction(DEC, 7)

def DEX(mos):
    mos["x"] -= 1
DEX_IMPLIED = ImpliedInstruction(DEX, 2)

def DEY(mos):
    mos["y"] -= 1
DEY_IMPLIED = ImpliedInstruction(DEY, 2)

def EOR(data, mos):
    mos["a"] = mos["a"] ^ a
EOR_IMMEDIATE = ImmediateInstruction(EOR, 2)
EOR_ABSOLUTE  = AbsoluteInstruction (EOR, 4)
EOR_ZEROPAGE  = ZeroPageInstruction (EOR, 3)
EOR_INDIRECTX = IndirectXInstruction(EOR, 6)
EOR_INDIRECTY = IndirectYInstruction(EOR, 5)
EOR_ZEROPAGEX = ZeroPageXInstruction(EOR, 4)
EOR_ABSOLUTEX = AbsoluteXInstruction(EOR, 4)
EOR_ABSOLUTEY = AbsoluteYInsturction(EOR, 4)

def INC(data, mos):
    return mos[data] + 1
INC_ABSOLUTE  = AbsoluteInstruction (INC, 6)
INC_ZEROPAGE  = ZeroPageInstruction (INC, 5)
INC_ZEROPAGEX = ZeroPageXInstruction(INC, 6)
INC_ABSOLUTEX = AbsoluteXInstruction(INC, 7)

def INX(mos):
    mos["x"] += 1
INX_IMPLIED = ImpliedInstruction(INX, 2)

def INY(mos):
    mos["y"] += 1
INY_IMPLIED = ImpliedInstruction(INY, 2)

def JMP(data, mos):
    mos["pc"] = data
JMP_ABSOLUTE = AbsoluteInstruction(JMP, 3)
JMP_INDIRECT = IndirectInstruction(JMP, 5)