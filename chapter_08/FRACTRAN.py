#
#  file:  FRACTRAN.py
#
#  An implementation of Conway's FRACTRAN.  Python 3.
#
#  RTK, 28-Jun-2020
#  Last update:  05-Apr-2021
#
###############################################################

import sys
from fractions import Fraction

def LoadProgram(fname):
    """Load a FRACTRAN program"""
    
    src = open(fname).read()
    eoln = False
    t = ""
    for c in src:
        if (eoln) and (c == "\n"):
            eoln = False
        elif (c == ";") and (not eoln):
            eoln = True
        elif (not eoln):
            t += c
    
    p = []
    t = t.split()
    for w in t:
        n,d = w.split("/")
        p.append(Fraction(int(n),int(d)))
    return p


def main():
    """Run the given FRACTRAN program"""

    if (len(sys.argv) == 1):
        print()
        print("FRACTRAN <file> <n> [0|1]")
        print()
        print("  <file> - comma separated sequence of fractions")
        print("  <n>    - starting value (integer)")
        print("  0|1    - 0=show final value only, 1=show sequence")
        print()
        return

    n = Fraction(int(sys.argv[2]))
    p = LoadProgram(sys.argv[1])
    m = int(sys.argv[3]) if (len(sys.argv) >= 4) else 0

    k = 0
    while (k < len(p)):
        v = n * p[k]
        if (v.denominator == 1):
            if (m):
                print(v)
            n = Fraction(v)
            k = -1
        k += 1

    if (not m):
        print(n)


if (__name__ == "__main__"):
    main()

