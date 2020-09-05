"""
http://archive.6502.org/datasheets/mos_6500_mpu_mar_1980.pdf
http://archive.6502.org/datasheets/mos_6500_mpu_nov_1985.pdf
http://pdf.datasheetcatalog.com/datasheet/UMC/mXyztwtz.pdf
"""
import os
import sys
import re

from mos6500 import MOS6500

if __name__ == "__main__":
    if sys.argv[1] == "debugger":
        with open(sys.argv[2], "rb") as f:
            rom = f.read()

        mos = MOS6500(65536)
        mos.load(rom)

        while True:
            print(mos)

            while True:
                ram_addr = input()

                if ram_addr == "":
                    break
                else:
                    try:
                        ram_addr = int(ram_addr, base=16)
                        print(f"RAM[{hex(ram_addr)}]: {mos.ram[ram_addr]}")
                    except ValueError:
                        print("Invalid syntax; try again.")

            os.system("cls" if os.name == "nt" else "clear")
            mos.exec(1)
    elif sys.argv[1] == "disassembler":
        with open(sys.argv[2], "rb") as f:
            rom = f.read()

        mos = MOS6500(65536)
        mos.load(rom)

        with open(f"{sys.argv[2].split('.')[0]}.asm", "w") as f:
            while True:
                try:
                    instruction, data = mos.read_instruction()
                except IndexError:
                    """
                    EOF
                    """
                    break
                except KeyError:
                    """
                    Non-instruction encountered; perhaps in a memory block.
                    """
                    continue

                f.write(f"{instruction.str(data)}\n")
    elif sys.argv[1] == "assembler":
        mos = MOS6500(0)

        ptrn = re.compile("[a-zA-Z0-9]+")
        with open(sys.argv[2], "r") as f, open(f"{sys.argv[2].split('.')[0]}.bin", "wb") as out:
            symbols = {}
            line = 1
            num_bytes = 0
            while True:
                asm = f.readline()
                if asm == "":
                    break
                elif asm == "\n":
                    continue

                parts = ptrn.findall(asm)

                # Symbol declaration
                if parts[0][0] == ":":
                    symbols[parts[0]] = num_bytes
                    continue

                opcode = parts[0]
                type = ""
                operands = []

                if len(parts) > 1:
                    type = parts[1]
                    operands = parts[2:]

                for i, instruction in enumerate(mos.instruction_set):
                    if instruction == 0:
                        continue

                    if instruction.name == str.upper(opcode) and instruction.type == str.lower(type):
                        opcode = i
                        break

                for i, operand in enumerate(operands):
                    # Is it a literal?
                    try:
                        operands[i] = int(operand, base=16)
                    except ValueError:
                        # If it's a symbol, retrieve the byte # that the symbol
                        # appeared
                        if operands[i] in symbols:
                            operands[i] = symbols[operands[i]]
                        else:
                            print(f"Error: unexpected symbol on line {line}\n")
                            sys.exit(1)

                out.write(bytes([opcode] + operands))

                line += 1
                num_bytes += 1 + len(operands)