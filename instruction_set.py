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
        self.fn(mos.ram[(data[1] << 8)] + data[0], mos)
class ZeroPageInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(mos.ram[data[0]], mos)
class AccumulatorInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn("a", mos)
class ImpliedInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(mos)
class IndirectXInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(
            mos.ram[
                mos.index_x + data[0] +
                ((mox.index_x + data[0] + 1) << 8)
            ],
            mos
        )
class IndirectYInstruction(Instruction):
    def __call__(self, data, mos):
        self.fn(
            mos.ram[
                mos.ram[data[0]] + mos.index_y +
                ((mos.ram[data[0] + 1] + mox.index_y) << 8)
            ],
            mos
        )
class ZeroPageXInstruction(Instruction):
    def __call__(self, data, mos):
class AbsoluteXInstruction(Instruction):
    pass
class AbsoluteYInsturction(Instruction):
    pass
class RelativeInstruction(Instruction):
    pass
class IndirectInstruction(Instruction):
    pass
class ZeroPageYInstruction(Instruction):
    pass

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
    pass

def ASL(data, mos):
    mos[data] = mos[data] << 1