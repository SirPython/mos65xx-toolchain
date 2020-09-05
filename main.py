"""
http://archive.6502.org/datasheets/mos_6500_mpu_mar_1980.pdf
http://archive.6502.org/datasheets/mos_6500_mpu_nov_1985.pdf
http://pdf.datasheetcatalog.com/datasheet/UMC/mXyztwtz.pdf
"""
import os
import ctypes

import instruction_set


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