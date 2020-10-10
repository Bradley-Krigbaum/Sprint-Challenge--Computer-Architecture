"""CPU functionality."""
import sys


class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.SP = self.reg[7]

        self.branchtable = {}
        self.branchtable[0b00000001] = self.HLT
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b01000111] = self.PRN
        self.branchtable[0b10100010] = self.MUL
        self.branchtable[0b01000101] = self.PUSH
        self.branchtable[0b01000110] = self.POP
        self.branchtable[0b01010100] = self.JMP
        self.branchtable[0b01010000] = self.CALL
        self.branchtable[0b00010001] = self.RET
        self.branchtable[0b10100111] = self.CMP
        self.branchtable[0b01010101] = self.JEQ
        self.branchtable[0b01010110] = self.JNE


    def HLT(self):
        print('HLT: TRUE... EXITING...\nEXITING COMPLETE')
        self.running = False

    def LDI(self):
        print('LDI...')
        register = self.ram[self.pc + 1]
        integer = self.ram[self.pc + 2]
        self.reg[register] = integer
        self.pc += 3

    def PRN(self):
        print('PRN REG: ', self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def MUL(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.ALU('MUL', reg_a, reg_b)
        self.pc += 3

    def PUSH(self):
        print('PUSHING...')
        target_reg = self.ram[self.pc + 1]
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.reg[target_reg]
        self.pc += 2

    def POP(self):
        print('POPPING...')
        target_reg = self.ram[self.pc + 1]
        self.reg[target_reg] = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1
        self.pc += 2

    def JMP(self):
        print('JMP...')
        self.pc = self.reg[self.ram[self.pc + 1]]

    def JEQ(self):
        print('JEQ...')
        if self.E == 1:
            self.JMP()
        else:
            self.pc += 2

    def JNE(self):
        print('JNE...')
        if self.E == 0:
            self.JMP()
        else:
            self.pc += 2

    def CMP(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.ALU('CMP', operand_a, operand_b)
        self.pc += 3

    def CALL(self):
        print('CALL...')
        addy = self.pc + 2
        self.reg[7] -= 1
        self.ram[self.reg[7]] = addy
        self.pc = self.reg[self.ram[self.pc + 1]]

    def RET(self):
        print('RET...')
        self.pc = self.ram[self.reg[7]]
        self.reg[7] += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""
        print("LOADING...")

        address = 0

        with open(filename) as file_pointer:
            for line in file_pointer:
                line_split = line.split("#")
                num = line_split[0].strip()
                if num == '':
                    continue
                value = int(num, 2)
                #print('load value: ', value)
                self.ram_write(value, address)
                address += 1

        print("LOADING COMPLETE")

    def ALU(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
            print('ALU OPERATION: ADD... COMPLETE')
        elif op == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]
            print('ALU OPERATION: SUB... COMPLETE')
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
            print('ALU OPERATION: MUL... COMPLETE')
        elif op == 'DIV':
            self.reg[reg_a] //= self.reg[reg_b]
            print('ALU OPERATION: DIV... COMPLETE')
        elif op == 'CMP':
            print('ALU OPERATION: CMP... COMPLETE')
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
                self.L = 0
                self.G = 0
            elif reg_a < reg_b:
                self.E = 0
                self.L = 1
                self.G = 0
            elif reg_a > reg_b:
                self.E = 0
                self.L = 0
                self.G = 1
            else:
                self.E = 0
                self.L = 0
                self.G = 0
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            IR = self.pc
            instructions = self.ram[IR]
            print('run instructions: ', instructions)
            self.branchtable[instructions]()
