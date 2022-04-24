#
#  file:  firefly_micro.py
#
#  Micro:bit version of Firefly.  Python 3.
#
#  RTK, 31-Aug-2020
#  Last update:  09-Jan-2021
#
################################################################

# Place your program code here without extra characters:
PRG = """
1TJ0TITFTFTFTFTFTFTF5TG8TJ1TFH
"""

from microbit import display
from music import play
from time import sleep
from random import randint

DIGITS = ["0","1","2","3","4","5","6","7","8","9"]
MOVES = ["N","E","W","T","S","L"]
BUFS = ["A","B","X","Y"]

A = bytearray(25)
B = bytearray(25)
C = A
D = A
M = "M"
I = 12
dur = 4
oc = 4
display.clear()

def Move(c):
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
    global C
    k = 0
    while k < 25:
        C[k] = 0
        k += 1

def ClearA():
    global A
    k = 0
    while k < 25:
        A[k] = 0
        k += 1

def ClearB():
    global B
    k = 0
    while k < 25:
        B[k] = 0
        k += 1

def Update():
    i = 0
    while i < 25:
        display.set_pixel(i%5, i//5, D[i])
        i += 1

def Display(c):
    global C,D

    if c == "A":
        C = A
    elif c == "B":
        C = B
    elif c == "X":
        D = A
    elif c == "Y":
        D = B

def Play():
    note = ["R","C","D","E","F","G","A","B"][C[I] % 8]
    play("%s%d:%d" % (note,oc,dur))

R = True
while R:
    for c in PRG:
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
        elif c == "J":
            dur = C[I]
        elif c == "F":
            Play()
        elif c == "G":
            oc = C[I]
        Update()

    C = A
    D = A
    M = "M"
    I = 12
    display.clear()
