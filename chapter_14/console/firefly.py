#
#  file:  firefly.py
#
#  Console version of Firefly.  Python 3.
#
#  RTK, 23-Aug-2020
#  Last update:  12-Jan-2021
#
################################################################

import sys
from time import sleep
from random import randint
import signal

TRACE = False
T = ""

#  Command lists
DIGITS = ["0","1","2","3","4","5","6","7","8","9"]
MOVES = ["N","E","W","T","S","L"]
BUFS = ["A","B","X","Y","V","Z"]
SOUND = ["J","G","F"]

#  Allowed program characters
ALLOWED = DIGITS + MOVES + BUFS + SOUND + ["I","D","M","H","P","C","R"]

A = bytearray(25)   # memory buffers
B = bytearray(25)
C = A               # work with buffer A
D = A               # show buffer A
M = "M"             # no trail
PRG = ""            # hold program text
I = 12              # start at (2,2) 
ZC = " "            # character to output for zero

def ctrlC(sig, frame):
    print("\nGoodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, ctrlC)


def Move(c):
    """Move according to the current mode"""

    global I,C

    #  Apply current mode
    if M == "M":
        pass
    elif M == "I":
        C[I] += 1
        if C[I] > 9:
            C[I] =0
    elif M == "D":
        if (C[I] == 0):
            C[I] = 9
        else:
            C[I] -= 1
    elif M == "R":
        C[I] = randint(1,9)
    else:
        C[I] = int(M)

    #  Now move somewhere
    i = I//5
    j = I%5

    if c == "N":
        i -= 1
        if i < 0:
            i = 4
    elif c == "S":
        i += 1
        if i > 4:
            i = 0
    elif c == "E":
        j += 1
        if j > 4:
            j = 0
    elif c == "W":
        j -= 1
        if j < 0:
            j = 4
    elif c == "T":
        pass
    elif c == "L":
        while True:
            sleep(1000)
    
    I = 5*i + j


def Clear():
    """Clear the currently active buffer"""

    global C

    k = 0
    while k < 25:
        C[k] = 0
        k += 1

def ClearA():
    """Clear A"""

    global A

    k = 0
    while k < 25:
        A[k] = 0
        k += 1

def ClearB():
    """Clear B"""

    global B

    k = 0
    while k < 25:
        B[k] = 0
        k += 1

#
#  Display functions for console version:
#
def Home():
    """Home the cursor"""
    print("%s[H" % chr(27), end="")


def ClearScreen():
    """Clear the screen"""
    print("%s[2J" % chr(27), end="")


def Trace():
    """Show the instruction in trace mode"""

    i = I//5; j = I%5
    b = "A" if C is A else "B"
    d = "A" if D is A else "B"
    print("I=(%d,%d)(%2d), SHOW=%s, DRAW=%s, M=%s, INST=%s" % (i,j,I,d,b,M,T))
    _ = input().lower()
    if (_ == "q"):
        print("\nGoodbye!")
        exit(0)


def Update():
    """Update the console display"""
    
    Home()
    print("    ", end="")
    i = 0
    while i < 25:
        if (D[i] != 0):
            print("%d " % D[i], end="")
        else:
            print("%s " % ZC, end="")
        if ((i+1) % 5 == 0):
            print("\n    ", end="")
        i += 1
    print()
    
    if TRACE:
        Trace()


def Display(c):
    """Process a display command"""

    global C,D

    if c == "A":
        C = A
    elif c == "B":
        C = B
    elif c == "X":
        D = A
    elif c == "Y":
        D = B


def Parse(prg):
    """Parse program text to remove all non-code"""

    t = ""
    inComment = False
    for c in prg:
        if c == "!" and not inComment:
            inComment = True
        elif c == "\n" and inComment:
            inComment = False
        elif not inComment:
            if c in ALLOWED:
                t += c
    return t


def main():
    """Run a Firefly program"""
   
    global PRG,M,TRACE,T,A,B,C,D,M,I,ZC

    if (len(sys.argv) == 1):
        print()
        print("firefly <prog> [-t] [-z]")
        print()
        print("  <prog>  -  Firefly program text (.fly)")
        print("  -t      -  trace mode on")
        print("  -z      -  show zeros")
        print()
        return

    TRACE = False
    for arg in sys.argv[2:]:
        if (arg == "-t"):
            TRACE = True
        if (arg == "-z"):
            ZC = "0"

    ClearScreen()
    
    PRG = Parse(open(sys.argv[1]).read().upper())
    R = True

    while R:
        for c in PRG:
            T = c
            if c == "I":
                M = "I"
            elif c == "D":
                M = "D"
            elif c == "M":
                M = "M"
            elif c == "R":
                M = "R"
            elif c in DIGITS:
                M = c
            elif c == "H":
                R = False
                break
            elif c in MOVES:
                Move(c)
            elif c == "P":
                sleep(0.1)
            elif c == "C":
                Clear()
            elif c == "V":
                ClearA()
            elif c == "Z":
                ClearB()
            elif c in BUFS:
                Display(c)

            #  for compatibility w/micro:bit version
            elif c == "J":
                pass
            elif c == "F":
                pass
            elif c == "G":
                pass
            Update()

        #  Reset to run in a loop
        C = A
        D = A
        M = "M"
        I = 12

    print("Goodbye!") 


if (__name__ == "__main__"):
    main()

