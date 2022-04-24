#
#  file:  fly_dump.py
#
#  Dump a simple string version of a Firefly program.
#
#  RTK, 01-Sep-2020
#  Last update:  16-Jan-2021
#
################################################################

import sys

DIGITS = ["0","1","2","3","4","5","6","7","8","9"]
MOVES = ["N","E","W","T","S","L"]
BUFS = ["A","B","X","Y","V","Z"]
SOUND = ["J","G","F"]
ALLOWED = DIGITS + MOVES + BUFS + SOUND + ["I","D","M","H","P","C","R"]

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
    """Dump a Firefly program"""
   
    if (len(sys.argv) == 1):
        print()
        print("fly_dump <prog> <out>")
        print()
        print("  <prog>  -  Firefly program text (.fly)")
        print("  <out>   -  Plain string program (.fly)")
        print()
        return

    prg = Parse(open(sys.argv[1]).read().upper())
    
    with open(sys.argv[2], "w") as f:
        f.write("%s" % prg)


if (__name__ == "__main__"):
    main()

