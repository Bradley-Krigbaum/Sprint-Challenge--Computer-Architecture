#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *


print("LS8 MACHINE RUNNING...")

if len(sys.argv) != 2:
    print("INCORRECT USAGE")
    sys.exit(1)

cpu = CPU()
cpu.load(sys.argv[1])
cpu.run()
