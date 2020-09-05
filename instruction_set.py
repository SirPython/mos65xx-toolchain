# todo: figure out indirect y, figure out carry bits and overflow stuff
# todo: all instructions of same type have same # of bytes

class Instruction():
    def __init__(self, fn, num_cycles, num_bytes, type):
        self.fn = fn
        self.num_cycles = num_cycles
        self.num_bytes = num_bytes
        self.type = type

        self.name = fn.__name__

    def mem_routine(self, addr, mos):
        """
        Some instructions modify the memory which with they interact. This
        function handles setting the memory value after the computations.
        """
        ret = self.fn(mos[addr], mos)

        if ret:
            mos[addr] = ret

    def str(self, data):
        return f"{self.name} {self.type}({','.join(map(hex, data))})"

class ImmediateInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2, "imm")

    def __call__(self, data, mos):
        self.fn(data[0], mos)

class AbsoluteInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 3, "abs")

    def __call__(self, data, mos):
        self.mem_routine(
            data[0] + (data[1] << 8),
            mos
        )
class ZeroPageInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2, "zp")

    def __call__(self, data, mos):
        self.mem_routine(data[0], mos)

class AccumulatorInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 1, "acc")

    def __call__(self, data, mos):
        self.fn("a", mos)

class ImpliedInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 1, "")

    def __call__(self, data, mos):
        self.fn(mos)

    def str(self, data):
        return f"{self.name}"
class IndirectXInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2, "ix")

    def __call__(self, data, mos):
        addr = data[0] + mos.index_x
        self.mem_routine(
            mos[addr] + (mos[addr + 1] << 8),
            mos
        )
class IndirectYInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2, "iy")

    def __call__(self, data, mos):
        self.mem_routine(
            mos[data[0]] + mos.index_y,
            mos
        )

class ZeroPageXInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2, "zpx")

    def __call__(self, data, mos):
        self.mem_routine(data[0] + mos.index_x, mos)

class AbsoluteXInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 3, "absx")

    def __call__(self, data, mos):
        self.mem_routine(data[0] + data[1] + mos.index_x, mos)

class AbsoluteYInsturction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 3, "absy")

    def __call__(self, data, mos):
        self.mem_routine(data[0] + data[1] + mos.index_y, mos)
class RelativeInstruction(Instruction):
    def __init__(self, name, status_flag, cond_val, num_cycles):
        self.status_flag = status_flag
        self.cond_val = cond_val

        self.num_cycles = num_cycles
        self.num_bytes = 2

        self.name = name

    def __call__(self, data, mos):
        if mos[self.status_flag] == self.cond_val:
            mos["pc"] = (mos["pc"] & 0xFF) + data[0]

    def str(self, data):
        return f"{self.name}"
class IndirectInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 3, "y")

    def __call__(self, data, mos):
        addr = data[0] + (data[1] << 8)
        self.fn(mos[addr] + (mos[addr + 1] << 8), mos)
class ZeroPageYInstruction(Instruction):
    def __init__(self, fn, num_cycles):
        super().__init__(fn, num_cycles, 2, "zpy")

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
    mos["carry"] = data & 0x7F
    return (data << 1) & 0xFF
ASL_ABSOLUTE    = AbsoluteInstruction   (ASL, 6)
ASL_ZEROPAGE    = ZeroPageInstruction   (ASL, 5)
ASL_ACCUMULATOR = AccumulatorInstruction(ASL, 2)
ASL_ZEROPAGEX   = ZeroPageXInstruction  (ASL, 6)
ASL_ABSOLUTEX   = AbsoluteXInstruction  (ASL, 7)

BCC_RELATIVE = RelativeInstruction("BCC", "carry", 0, 2)
BCS_RELATIVE = RelativeInstruction("BCS", "carry", 1, 2)
BEQ_RELATIVE = RelativeInstruction("BEQ", "zero",  1, 2)

def BIT(data, mos):
    res = (mos["a"] & data) << 6
    mos["overflow"] = res & 0x01
    mos["negative"] = res << 1
BIT_ABSOLUTE = AbsoluteInstruction(BIT, 4)
BIT_ZEROPAGE = ZeroPageInstruction(BIT, 3)

BMI_RELATIVE = RelativeInstruction("BMI", "negative", 1, 2)
BNE_RELATIVE = RelativeInstruction("BNE", "zero",     0, 2)
BPL_RELATIVE = RelativeInstruction("BPL", "negative", 0, 2)

def BRK(data, mos):
    print("****BREAK****")
BRK_IMPLIED = ImpliedInstruction(BRK, 7)

BVC_RELATIVE = RelativeInstruction("BVC", "overflow", 0, 2)
BVS_RELATIVE = RelativeInstruction("BVS", "overflow", 1, 2)

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
    return data - 1
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
    return data + 1
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

def JSR(data, mos):
    print("****JSR****")
JSR_ABSOLUTE = AbsoluteInstruction(JSR, 6)

def LDA(data, mos):
    mos["a"] = data
LDA_IMMEDIATE = ImmediateInstruction(LDA, 2)
LDA_ABSOLUTE  = AbsoluteInstruction (LDA, 4)
LDA_ZEROPAGE  = ZeroPageInstruction (LDA, 3)
LDA_INDIRECTX = IndirectXInstruction(LDA, 6)
LDA_INDIRECTY = IndirectYInstruction(LDA, 5)
LDA_ZEROPAGEX = ZeroPageXInstruction(LDA, 4)
LDA_ABSOLUTEX = AbsoluteXInstruction(LDA, 4)
LDA_ABSOLUTEY = AbsoluteYInsturction(LDA, 4)

def LDX(data, mos):
    mos["x"] = data
LDX_IMMEDIATE = ImmediateInstruction(LDX, 2)
LDX_ABSOLUTE  = AbsoluteInstruction (LDX, 4)
LDX_ZEROPAGE  = ZeroPageInstruction (LDX, 3)
LDX_ABSOLUTEY = AbsoluteYInsturction(LDX, 4)
LDX_ZEROPAGEY = ZeroPageYInstruction(LDX, 4)

def LDY(data, mos):
    mos["y"] = data
LDY_IMMEDIATE = ImmediateInstruction(LDY, 2)
LDY_ABSOLUTE  = AbsoluteInstruction (LDY, 4)
LDY_ZEROPAGE  = ZeroPageInstruction (LDY, 3)
LDY_ZEROPAGEX = ZeroPageXInstruction(LDY, 4)
LDY_ABSOLUTEX = AbsoluteXInstruction(LDY, 4)

def LSR(data, mos):
    mos["carry"] = data & 0x01
    return data >> 1
LSR_ABSOLUTE    = AbsoluteInstruction   (LSR, 6)
LSR_ZEROPAGE    = ZeroPageInstruction   (LSR, 5)
LSR_ACCUMULATOR = AccumulatorInstruction(LSR, 2)
LSR_ZEROPAGEX   = ZeroPageXInstruction  (LSR, 6)
LSR_ABSOLUTEX   = AbsoluteXInstruction  (LSR, 7)

def NOP(mos):
    pass
NOP_IMPLIED = ImpliedInstruction(NOP, 2)

def ORA(data, mos):
    mos["a"] = mos["a"] | a
ORA_IMMEDIATE = ImmediateInstruction(ORA, 2)
ORA_ABSOLUTE  = AbsoluteInstruction (ORA, 4)
ORA_ZEROPAGE  = ZeroPageInstruction (ORA, 3)
ORA_INDIRECTX = IndirectXInstruction(ORA, 6)
ORA_INDIRECTY = IndirectYInstruction(ORA, 5)
ORA_ZEROPAGEX = ZeroPageXInstruction(ORA, 4)
ORA_ABSOLUTEX = AbsoluteXInstruction(ORA, 4)
ORA_ABSOLUTEY = AbsoluteYInsturction(ORA, 4)

def push(addr, mos):
    mos[mos["s"]] = mos[addr]
    mos["s"] -= 1
def pull(addr, mos):
    mos["s"] += 1
    mos[addr] = mos[mos["s"]]

def PHA(mos):
    push("a", mos)
PHA_IMPLIED = ImpliedInstruction(PHA, 3)

def PHP(mos):
    push("status", mos)
PHP_IMPLIED = ImpliedInstruction(PHP, 3)

def PLA(mos):
    pull("a", mos)
PLA_IMPLIED = ImpliedInstruction(PLA, 4)

def PLP(mos):
    pull("status", mos)
PLP_IMPLIED = ImpliedInstruction(PLP, 4)

def ROL(data, mos):
    old_carry = mos["carry"]
    mos["carry"] = data >> 7

    return ((data << 1) & 0xFF) | old_carry
ROL_ABSOLUTE    = AbsoluteInstruction   (ROL, 6)
ROL_ZEROPAGE    = ZeroPageInstruction   (ROL, 5)
ROL_ACCUMULATOR = AccumulatorInstruction(ROL, 2)
ROL_ZEROPAGEX   = ZeroPageXInstruction  (ROL, 6)
ROL_ABSOLUTEX   = AbsoluteXInstruction  (ROL, 7)

def ROR(data, mos):
    old_carry = mos["carry"]
    mos["carry"] = data & 0x01

    return (data >> 1) | (old_carry << 7)
ROR_ABSOLUTE    = AbsoluteInstruction   (ROR, 6)
ROR_ZEROPAGE    = ZeroPageInstruction   (ROR, 5)
ROR_ACCUMULATOR = AccumulatorInstruction(ROR, 2)
ROR_ZEROPAGEX   = ZeroPageXInstruction  (ROR, 6)
ROR_ABSOLUTEX   = AbsoluteXInstruction  (ROR, 7)

def RTI(mos):
    print("****RTI****")
RTI_IMPLIED = ImpliedInstruction(RTI, 6)

def RTS(mos):
    print("****RTS****")
RTS_IMPLIED = ImpliedInstruction(RTS, 6)

def SBC(data, mos):
    mos["a"] = mos["a"] - data - mos["carry"]
SBC_IMMEDIATE = ImmediateInstruction(SBC, 2)
SBC_ABSOLUTE  = AbsoluteInstruction (SBC, 4)
SBC_ZEROPAGE  = ZeroPageInstruction (SBC, 3)
SBC_INDIRECTX = IndirectXInstruction(SBC, 6)
SBC_INDIRECTY = IndirectYInstruction(SBC, 5)
SBC_ZEROPAGEX = ZeroPageXInstruction(SBC, 4)
SBC_ABSOLUTEX = AbsoluteXInstruction(SBC, 4)
SBC_ABSOLUTEY = AbsoluteYInsturction(SBC, 4)

def SEC(mos):
    mos["carry"] = 1
SEC_IMPLIED = ImpliedInstruction(SEC, 2)

def SED(mos):
    mos["decimal_mode"] = 1
SED_IMPLIED = ImpliedInstruction(SED, 2)

def SEI(mos):
    mos["irq_disable"] = 1
SEI_IMPLIED = ImpliedInstruction(SEI, 2)

def STA(data, mos):
    return mos["a"]
STA_ABSOLUTE  = AbsoluteInstruction (STA, 4)
STA_ZEROPAGE  = ZeroPageInstruction (STA, 3)
STA_INDIRECTX = IndirectXInstruction(STA, 6)
STA_INDIRECTY = IndirectYInstruction(STA, 6)
STA_ZEROPAGEX = ZeroPageXInstruction(STA, 4)
STA_ABSOLUTEX = AbsoluteXInstruction(STA, 5)
STA_ABSOLUTEY = AbsoluteYInsturction(STA, 5)

def STX(data, mos):
    return mos["x"]
STX_ABSOLUTE  = AbsoluteInstruction (STX, 4)
STX_ZEROPAGE  = ZeroPageInstruction (STX, 3)
STX_ZEROPAGEY = ZeroPageYInstruction(STX, 4)


def STY(data, mos):
    return mos["y"]
STY_ABSOLUTE  = AbsoluteInstruction (STY, 4)
STY_ZEROPAGE  = ZeroPageInstruction (STY, 3)
STY_ZEROPAGEX = ZeroPageXInstruction(STY, 4)

def TAX(mos):
    mos["x"] = mos["a"]
TAX_IMPLIED = ImpliedInstruction(TAX, 2)

def TAY(mos):
    mos["y"] = mos["a"]
TAY_IMPLIED = ImpliedInstruction(TAY, 2)

def TSX(mos):
    mos["x"] = mos["s"]
TSX_IMPLIED = ImpliedInstruction(TSX, 2)

def TXA(mos):
    mos["a"] = mos["x"]
TXA_IMPLIED = ImpliedInstruction(TXA, 2)

def TXS(mos):
    mos["s"] = mos["x"]
TXS_IMPLIED = ImpliedInstruction(TXS, 2)

def TYA(mos):
    mos["a"] = mos["y"]
TYA_IMPLIED = ImpliedInstruction(TYA, 2)