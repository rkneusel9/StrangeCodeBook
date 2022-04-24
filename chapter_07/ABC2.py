#!/usr/bin/python3
#
#  file:  ABC2.py
#
#  An interpreter for the extended ABC language.
#
#  RTK, 27-Jun-2020
#  Last update:  09-Mar-2021
#
################################################################

import sys
import random

################################################################
#  OS-specific way to get a character w/o newline
#
class _Getch:
    """Gets a single character from standard input"""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()


################################################################
#  main
#
def main():
    """Interpret an ABC2 program"""

    if (len(sys.argv)==2):
        interactive = False
        t = open(sys.argv[1]).read()
        tokens = [
            "a","b","c","d","r","n","$","l",";",
            "e",">","<","g","+","-","*","/","x",
            "q","%","=","?","!","@","k","^",
        ]
        prog = ""
        for c in t:
            if (c in tokens):
                prog += c
    else:
        interactive = True
        
    A = [0,0]
    I = mode = cr = k = 0
    stack = []
    ops = ["+","-","*","/","%","<",">","="]

    while (True):
        if (interactive):
            prog = input(": ")
            k = 0
        while (k < len(prog)):
            t = prog[k]
            if (t == "a"):
                A[I] += 1
            elif (t == "b"):
                A[I] -= 1
            elif (t == "c"):
                if (mode):
                    print("%s" % chr(A[I]), end="", flush=True)
                else:
                    print("%d" % A[I], end="", flush=True)
                if (cr):
                    print()
            elif (t == "d"):
                A[I] = -A[I]
            elif (t == "r"):
                A[I] = int(random.random()*A[I])
            elif (t == "n"):
                A[I] = 0
            elif (t == "$"):
                mode ^= 1
            elif (t == "l"):
                k = -1
            elif (t == ";"):
                c0 = chr(A[0]) if (31 < A[0] < 128) else ""
                c1 = chr(A[1]) if (31 < A[1] < 128) else ""
                print("{%d:%d: (%d,'%s')(%d,'%s')} " % (k, I, A[0], c0, A[1], c1), end="")
                print("<%d>: " % len(stack), end="")
                for s in stack:
                    print("%d " % s, end="")
                print()

            #  extensions:
            elif (t == "^"):
                I ^= 1
            elif (t == "k"):
                A[I] = ord(getch())
            elif (t == "q"):
                quit()
            elif (t == "e"):
                cr ^= 1
            elif (t == "!"):
                stack.append(A[I])
            elif (t == "@"):
                if (len(stack) != 0):
                    A[I] = stack.pop()
            elif (t == "g"):
                if (len(stack) != 0):
                    k = k + stack.pop() - 1
            elif (t == "?"):
                if (len(stack) != 0):
                    if (not stack.pop()):
                        k = k + 1
            elif (t == "x"):
                if (len(stack) != 0):
                    v = stack.pop()
                    stack.append(A[I])
                    A[I] = v
            elif (t in ops):
                if (t == "="):
                    t = "=="
                v = eval("%d %s %d" % (stack[-2],t,stack[-1]))
                if (type(v) is bool):
                    v = 1 if (v) else 0
                stack.pop(); stack.pop()
                stack.append(int(v))
            else:
                pass
            k += 1
        if (not interactive):
            print()
            quit()


if (__name__ == "__main__"):
    main()

