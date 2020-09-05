"""
http://archive.6502.org/datasheets/mos_6500_mpu_mar_1980.pdf
http://archive.6502.org/datasheets/mos_6500_mpu_nov_1985.pdf
http://pdf.datasheetcatalog.com/datasheet/UMC/mXyztwtz.pdf
"""
import os
import sys

from mos6500 import MOS6500


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        rom = f.read()

    mos = MOS6500()
    mos.load(rom)

    while True:
        print(mos)

        while True:
            ram_addr = input()

            if ram_addr == "":
                break
            else:
                ram_addr = int(ram_addr)
                print(f"RAM[{ram_addr}]: {mos.ram[ram_addr]}")

        os.system("cls" if os.name == "nt" else "clear")
        mos.exec(1)