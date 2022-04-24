#
#  file:  filska.py
#
#  Filska interpreter.  Python 3.
#
#  RTK, 05-Jul-2020
#  Last update:  07-Feb-2022
#
################################################################

import sys
import time
import random
import signal

from math import fmod, ceil, floor, sqrt
from math import sin, cos, tan, log, exp, pow, asin, acos, atan


################################################################
#  ctrlC
#
def ctrlC(sig, frame):
    print()
    sys.exit(0)

signal.signal(signal.SIGINT, ctrlC)


################################################################
#  Filska
#
class Filska:
    """Implement a Filska machine and interpreter"""

    #-----------------------------------------------------------
    #  Parse
    #
    def Parse(self, src):
        """
        Parse Filska source code
        """

        eoln = False
        t = ""
        for c in src:
            if (eoln) and (c == '\n'):
                eoln = False
            elif (c == '"') and (not eoln):
                eoln = True
            elif (not eoln):
                t += c
        return " ".join(t.split()).upper().split()


    #-----------------------------------------------------------
    #  ExtractProg
    #
    def ExtractProg(self, tokens, ks):
        """Extract a program"""

        k = ks + 1
        p = []
        while (k < len(tokens)) and (tokens[k] != "}"):
            p.append(tokens[k])
            k += 1
        self.prog[p[0]] = p[1:]
        self.PC[p[0]] = 0
        self.mem[p[0]] = 0.0
        self.flags[p[0]] = [False, False, False, False]
        return k


    #-----------------------------------------------------------
    #  InitializeProg
    #
    def InitializeProg(self, tokens):
        """Scan the tokens to set up the program space"""

        idx = 0
        k = 0
        while (k < len(tokens)):
            if (tokens[k] == "{"):
                k = self.ExtractProg(tokens,k)
            else:
                k += 1


    #-----------------------------------------------------------
    #  Trace
    #
    def Trace(self):
        """Show the next instruction in trace mode"""

        prog = self.prog[self.CP]
        pc = self.PC[self.CP]
        flags = self.flags[self.CP]
        mem = self.mem[self.CP]
        inst = prog[pc]
        print("CP:%s,PC:%03d,X:%f,Y:%f,Z:%f,M:%f" % (self.CP, pc, self.X, self.Y, self.Z, mem), end="")
        Z = 1 if (flags[0]) else 0
        E = 1 if (flags[1]) else 0
        L = 1 if (flags[2]) else 0
        G = 1 if (flags[3]) else 0
        print(",Z:%d,E:%d,L:%d,G:%d, %7s" % (Z,E,L,G, inst))
        _ = input("<enter> or 'q' to quit: ").lower()
        if (_ == "q"):
            exit(0)

    
    #-----------------------------------------------------------
    #  Instructions
    #
    def INC(self, rest, mem, flags):
        mem += 1
        flags[0] = False
        if (mem == 0):
            flags[0] = True
        return mem, flags

    def DEC(self, rest, mem, flags):
        mem -= 1
        flags[0] = False
        if (mem == 0):
            flags[0] = True
        return mem, flags

    def SET(self, rest, mem, flags):
        try:
            n = float(rest)
        except:
            n = 0.0
        mem = n
        flags[0] = False
        if (mem == 0):
            flags[0] = True
        return mem, flags

    def RND(self, rest, mem, flags):
        mem = random.random()
        return mem, flags

    def HLT(self, rest, mem, flags):
        print()
        exit(0)

    #  Binary operators
    #   rest is "<dst>=<op1><op2>, e.g., y=mx"
    #
    def ops(self, rest, mem):
        if (len(rest) != 4) or (rest[1] != "="):
            raise ValueError("Illegal operands: %s" % rest)
        dst = rest[0]
        op0 = op1 = 0.0
        if (rest[2] == "M"):
            op0 = mem
        elif (rest[2] == "X"):
            op0 = self.X
        elif (rest[2] == "Y"):
            op0 = self.Y
        elif (rest[2] == "Z"):
            op0 = self.Z
        if (rest[3] == "M"):
            op1 = mem
        elif (rest[3] == "X"):
            op1 = self.X
        elif (rest[3] == "Y"):
            op1 = self.Y
        elif (rest[3] == "Z"):
            op1 = self.Z
        return op0, op1, dst

    def assign(self, ans, dst, mem, flags):
        if (dst == "M"):
            mem = ans
            flags[0] = False
            if (mem == 0):
                flags[0] = True
        elif (dst == "X"):
            self.X = ans
        elif (dst == "Y"):
            self.Y = ans
        else:
            self.Z = ans
        return mem, flags

    def ADD(self, rest, mem, flags):
        op0,op1,dst = self.ops(rest,mem)
        ans = op0 + op1
        return self.assign(ans, dst, mem, flags)

    def SUB(self, rest, mem, flags):
        op0,op1,dst = self.ops(rest,mem)
        ans = op0 - op1
        return self.assign(ans, dst, mem, flags)

    def MUL(self, rest, mem, flags):
        op0,op1,dst = self.ops(rest,mem)
        ans = op0 * op1
        return self.assign(ans, dst, mem, flags)

    def DIV(self, rest, mem, flags):
        op0,op1,dst = self.ops(rest,mem)
        ans = op0 / op1
        return self.assign(ans, dst, mem, flags)

    def MOD(self, rest, mem, flags):
        op0,op1,dst = self.ops(rest,mem)
        ans = fmod(op0, op1)
        return self.assign(ans, dst, mem, flags)

    def POW(self, rest, mem, flags):
        op0,op1,dst = self.ops(rest,mem)
        ans = pow(op0, op1)
        return self.assign(ans, dst, mem, flags)

    #  Unary operators -- memory only
    def SQR(self, rest, mem, flags):
        try:
            mem = sqrt(mem)
        except:
            mem = 0.0  # real only
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def NEG(self, rest, mem, flags):
        mem = -mem
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def SIN(self, rest, mem, flags):
        mem = sin(mem)
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def COS(self, rest, mem, flags):
        mem = cos(mem)
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def TAN(self, rest, mem, flags):
        mem = tan(mem)
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def ASN(self, rest, mem, flags):
        mem = asin(mem)
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def ACS(self, rest, mem, flags):
        mem = acos(mem)
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def ATN(self, rest, mem, flags):
        mem = atan(mem)
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def LOG(self, rest, mem, flags):
        try:
            mem = log(mem)
        except:
            mem = 0.0
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def EXP(self, rest, mem, flags):
        mem = exp(mem)
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def FLR(self, rest, mem, flags):
        mem = floor(mem)
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def CEL(self, rest, mem, flags):
        mem = ceil(mem)
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def SWP(self, rest, mem, flags):
        if (rest == "MX") or (rest == "XM"):
            t = mem; mem = self.X; self.X = t
        elif (rest == "MY") or (rest == "YM"):
            t = mem; mem = self.Y; self.Y = t
        elif (rest == "MZ") or (rest == "ZM"):
            t = mem; mem = self.Z; self.Z = t
        elif (rest == "XY") or (rest == "YX"):
            t = self.X; self.X = self.Y; self.Y = t
        elif (rest == "XZ") or (rest == "ZX"):
            t = self.X; self.X = self.Z; self.Z = t
        elif (rest == "YZ") or (rest == "ZY"):
            t = self.Y; self.Y = self.Z; self.Z = t
        else:
            raise ValueError("Illegal SWP command")
        flags[0] = False
        if (mem == 0):
            flags[0] = True
        return mem, flags

    def TMX(self, rest, mem, flags):
        self.X = mem
        return mem, flags

    def TMY(self, rest, mem, flags):
        self.Y = mem
        return mem, flags

    def TMZ(self, rest, mem, flags):
        self.Z = mem
        return mem, flags

    def TXM(self, rest, mem, flags):
        mem = self.X
        if (mem == 0):
            flags[0] = True
        return mem, flags

    def TYM(self, rest, mem, flags):
        mem = self.Y
        if (mem == 0):
            flags[0] = True
        return mem, flags
    
    def TZM(self, rest, mem, flags):
        mem =self.Z
        if (mem == 0):
            flags[0] = True
        return mem, flags

    def CHR(self, rest, mem, flags):
        n = int(mem) & 255
        if (n == 10) or (n == 13):
            print()
        else:
            w = chr(n)
            print("%s" % w, end="")
        return mem, flags

    def PRT(self, rest, mem, flags):
        if (mem == int(mem)):
            print("%d" % int(mem), end="")
        else:
            print("%0.10g" % mem, end="")
        return mem, flags
    
    def IPT(self, rest, mem, flags):
        try:
            t = input()
        except:
            print()
            exit(0)
        try:
            mem = float(t)
        except:
            mem = 0.0
        flags[0] = False
        if (mem == 0.0):
            flags[0] = True
        return mem, flags

    def CMP(self, rest, mem, flags):
        if (rest == "X"):
            n = self.X
        elif (rest == "Y"):
            n = self.Y
        elif (rest == "Z"):
            n = self.Z
        else:
            try:
                n = float(rest)
            except:
                n = 0
        #        Z      E      L      G
        flags = [False, False, False, False]
        if (mem < n):
            flags[2] = True
        if (mem > n):
            flags[3] = True
        if (n == mem):
            flags[1] = True
        if (mem == 0):
            flags[0] = True
        return mem, flags

    def JMP(self, inst, pc, proglen):
        pc = (pc+1) % proglen
        cp = inst[4:]
        return pc, cp

    def JPR(self, inst, pc):
        pc = 0
        cp = inst[4:]
        return pc, cp

    def GTO(self, inst, pc, proglen):
        try:
            offset = int(inst[4:])
            if (offset == 0):
                offset = 1
        except:
            offset = 1
        pc += offset
        if (pc < 0):
            pc = 0
        if (pc >= proglen):
            pc = proglen-1
        return pc
        
    def TST(self, inst, pc, proglen, flags):
        if (inst[4] == "Z"):
            v = flags[0]
        elif (inst[4] == "E"):
            v = flags[1]
        elif (inst[4] == "L"):
            v = flags[2]
        elif (inst[4] == "G"):
            v = flags[3]
        elif (inst[4] == "N"):
            v = (flags[0] == False)
        if (v):
            try:
                offset = int(inst[6:])
                if (offset == 0):
                    offset = 1
            except:
                offset = 1
            pc += offset
            if (pc < 0):
                pc = 0
            if (pc >= proglen):
                pc = proglen-1
        else:
            pc = (pc+1) % proglen
        return pc


    #-----------------------------------------------------------
    #  Exec
    #
    def Exec(self, inst, proglen, mem, pc, flags):
        """Execute the instruction and return new state"""

        cp = self.CP
        if (inst[:3] == "JMP"):
            pc, cp = self.JMP(inst, pc, proglen)
        elif (inst[:3] == "JPR"):
            pc, cp = self.JPR(inst, pc)
        elif (inst[:3] == "GTO"):
            pc = self.GTO(inst, pc, proglen)
        elif (inst[:3] == "TST"):
            pc = self.TST(inst, pc, proglen, flags)
        else:
            if (inst[:3] not in self.exe):
                raise ValueError("Illegal instruction: %s" % inst)
            rest = inst[4:]
            mem, flags = self.exe[inst[:3]](rest, mem, flags)
            pc = (pc+1) % proglen

        return cp, pc, mem, flags 


    #-----------------------------------------------------------
    #  Execute
    #
    def Execute(self):
        """Execute one instruction"""

        #  Get the instruction and state
        prog = self.prog[self.CP]
        pc = self.PC[self.CP]
        flags = self.flags[self.CP]
        mem = self.mem[self.CP]
        inst = prog[pc]

        #  Execute it
        cp, pc, mem, flags = self.Exec(inst, len(prog), mem, pc, flags)

        #  Update the state
        self.mem[self.CP] = mem
        self.PC[self.CP] = pc
        self.flags[self.CP] = flags

        #  Move to any new program if cp changed -- reset flags
        if (self.CP != cp):
            self.CP = cp
            self.flags[cp] = [False, False, False, False]


    #-----------------------------------------------------------
    #  Run
    #
    def Run(self):
        """Run the program in memory"""

        if (self.trace):
            self.Trace()

        while (True):
            self.Execute()               # execute one instruction
            if (self.trace):             # trace, if set
                self.Trace()
            time.sleep(self.naptime)     # take a nap


    #-----------------------------------------------------------
    #  __init__
    #
    def __init__(self, src, trace=False):
        """Constructor"""

        #  Trace or not - console only
        self.trace = trace

        #  Controls program execution speed
        self.naptime = 0.00001  # seconds

        #  Set up the machine state
        self.X = self.Y = self.Z = 0    # global registers
        self.mem = {}
        self.prog = {}
        self.PC = {}
        self.CP = "MAIN"

        #  Per program flags:
        #       Z,E,L,G
        self.flags = {}

        #  Instructions
        self.exe = {
            "ADD": self.ADD,  "SUB": self.SUB,
            "MUL": self.MUL,  "DIV": self.DIV,
            "MOD": self.MOD,  "INC": self.INC,
            "DEC": self.DEC,  "SIN": self.SIN,
            "COS": self.COS,  "TAN": self.TAN,
            "LOG": self.LOG,  "EXP": self.EXP,
            "FLR": self.FLR,  "CEL": self.CEL,
            "RND": self.RND,  "SWP": self.SWP,
            "SET": self.SET,  "CMP": self.CMP,
            "NEG": self.NEG,  "HLT": self.HLT,
            "CHR": self.CHR,  "PRT": self.PRT,
            "IPT": self.IPT,  "POW": self.POW,
            "TMX": self.TMX,  "TMY": self.TMY,
            "TXM": self.TXM,  "TYM": self.TYM,
            "TZM": self.TZM,  "TMZ": self.TMZ,
            "SQR": self.SQR,  "ASN": self.ASN,
            "ACS": self.ACS,  "ATN": self.ATN,
        }

        #  Set up memory and program space
        self.tokens = self.Parse(src)
        self.InitializeProg(self.tokens)


################################################################
#  main
#
def main():
    """Run a Filska program"""

    if (len(sys.argv) == 1):
        print()
        print("filska <code> [-t]")
        print()
        print("  <code>   - the Filska program to run (.filska)")
        print("  -t       - trace mode on")
        print()
        return

    trace = False if (len(sys.argv) < 3) else True
    app = Filska(open(sys.argv[1]).read(), trace=trace)
    app.Run()


if (__name__ == "__main__"):
    main()

