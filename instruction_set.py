# TODO make subclasses of this for each type of instruction
class Instruction():
    def __init__(self, fn, num_cycles, num_bytes):
        self.fn = fn
        self.num_cycles = num_cycles
        self.num_bytes = num_bytes

    def __call__(self, data, mos):
        self.fn()

class ImmediateInstruction(Instruction):
    pass

class AbsoluteInstruction(Instruction):
    pass

class ZeroPageInstruction(Instruction):
    pass

class AccumulatorInstruction(Instruction):
    pass

class ImpliedInstruction(Instruction):
    pass

class IndirectXInstruction(Instruction):
    pass

class IndirectYInstruction(Instruction):
    pass

class ZeroPageXInstruction(Instruction):
    pass

class AbsoluteXInstruction(Instruction):
    pass

class AbsolutelYInsturction(Instruction):
    pass

class RelativeInstruction(Instruction):
    pass

class IndirectInstruction(Instruction):
    pass

class ZeroPageYInstruction(Instruction):
    pass


def ADC(data, mos):
    pass
ADC_IMMEDIATE = ImmediateInstruction(ADC, 2, 2)
ADC_ABSOLUTE  = AbsoluteInstruction (ADC, 4, 3)
ADC_ZEROPAGE  = ZeroPageInstruction (ADC, 3, 2)