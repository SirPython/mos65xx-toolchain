# todo: figure out indirect y, figure out carry bits and overflow stuff

class Instruction():
    def __init__(self, fn, num_cycles, num_bytes):
        self.fn = fn
        self.num_cycles = num_cycles
        self.num_bytes = num_bytes

class ImmediateInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(data[0], mos)
        pass
class AbsoluteInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(
            mos[
                data[0] +
                (data[1] << 8)
            ],
            mos
        )
class ZeroPageInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(mos[data[0]], mos)
class AccumulatorInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn("a", mos)
class ImpliedInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(mos)
class IndirectXInstruction(Instruction):
    def __call__(self, data, mos):
        addr = data[0] + mos.index_x
        self.fn(
            mos[
                mos[addr] +
                (mos[addr + 1] << 8)
            ],
            mos
        )
class IndirectYInstruction(Instruction):
    def __call__(self, data, mos):
        addr = mos[data[0]] + mos.index_y
        self.fn(
            mos[addr],
            mos
        )
class ZeroPageXInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(mos[data[0] + mos.index_x], mos)
class AbsoluteXInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(mos[data[0] + data[1] + mos.index_x], mos)
class AbsoluteYInsturction(Instruction):
    def __call__(self, data, mos):
        self.fn(mos[data[0] + data[1] + mos.index_y], mos)
class RelativeInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(data[0], mos)
class IndirectInstruction(Instruction):
    def __call__(self, data, mos):
        addr = data[0] + (data[1] << 8)
        mos.program_counter = mos[addr] + (mos[addr + 1] << 8)
class ZeroPageYInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(mos[data[0] + mos.index_y], mos)

def ADC(data, mos):
    mos.accumulator += data
ADC_IMMEDIATE = ImmediateInstruction(ADC, 2, 2)
ADC_ABSOLUTE  = AbsoluteInstruction (ADC, 4, 3)
ADC_ZEROPAGE  = ZeroPageInstruction (ADC, 3, 2)
ADC_INDIRECTX = IndirectXInstruction(ADC, 6, 2)
ADC_INDIRECTY = IndirectYInstruction(ADC, 6, 2)
ADC_ZEROPAGEX = ZeroPageXInstruction(ADC, 4, 2)
ADC_ABSOLUTEX = AbsoluteXInstruction(ADC, 4, 3)
ADC_ABSOLUTEY = AbsoluteYInsturction(ADC, 4, 3)

def AND(data, mos):
    mos.accumulator = mos.accumulator & data
AND_IMMEDIATE = ImmediateInstruction(AND, 2, 2)
AND_ABSOLUTE  = AbsoluteInstruction (AND, 4, 3)
AND_ZEROPAGE  = ZeroPageInstruction (AND, 3, 2)
AND_INDIRECTX = IndirectXInstruction(AND, 6, 2)
AND_INDIRECTY = IndirectYInstruction(AND, 6, 2)
AND_ZEROPAGEX = ZeroPageXInstruction(AND, 4, 2)
AND_ABSOLUTEX = AbsoluteXInstruction(AND, 4, 3)
AND_ABSOLUTEY = AbsoluteYInsturction(AND, 4, 3)

def ASL(data, mos):
    mos[data] = (mos[data] << 1) & 255
    mos["carry"] = mos[data] & 127
ASL_ABSOLUTE    = AbsoluteInstruction   (ASL, 6, 3)
ASL_ZEROPAGE    = ZeroPageInstruction   (ASL, 5, 2)
ASL_ACCUMULATOR = AccumulatorInstruction(ASL, 2, 1)
ASL_ZEROPAGEX   = ZeroPageXInstruction  (6, 2)
ASL_ABSOLUTEX   = AbsoluteXInstruction  (7, 3)
