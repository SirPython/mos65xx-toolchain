"""
http://archive.6502.org/datasheets/mos_6500_mpu_mar_1980.pdf
http://archive.6502.org/datasheets/mos_6500_mpu_nov_1985.pdf
http://pdf.datasheetcatalog.com/datasheet/UMC/mXyztwtz.pdf
"""
import os
import sys

from mos6500 import MOS6500


""" JUST MAKE THIS A PROPER ASSEMBLER, DISASSEMBLER, LINKER, DEBUGGER COMBO """

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
                except (IndexError, KeyError):
                    """
                    Reached when the end of the file has been met, or when
                    an invalid opcode is encountered.
                    """
                    break

                f.write(f"{instruction.str(data)}\n")
    elif sys.argv[1] == "assembler":
        pass