#!/usr/bin/python3
#
#  file:  ABC.py
#
#  An interpreter for the simple ABC language.
#
#  RTK, 27-Jun-2020
#  Last update:  27-Jun-2020
#
################################################################

import sys
import random

if (len(sys.argv)==1):
    print()
    print("ABC <file>")
    print()
    print("  <file> - ABC program to run")
    print()
    quit()

t=open(sys.argv[1]).read()
tokens=["a","b","c","d","r","n","$","l",";"]
prog=""
for c in t:
  if (c in tokens): prog+=c
mode=False; A=0; k=0
while (k<len(prog)):
  t=prog[k]
  if   (t=="a"): A+=1
  elif (t=="b"): A-=1
  elif (t=="c"): 
    if (mode):   print("%s"%chr(A),end="")
    else:        print("%d"%A,end="")
  elif (t=="d"): A=-A
  elif (t=="r"): A=int(random.random()*A)
  elif (t=="n"): A=0
  elif (t=="$"): mode=not mode
  elif (t=="l"): k=-1
  elif (t==";"): print("{%d:(%d,%x,'%s')}"%(k,A,A,chr(A)),end="")
  else:          pass
  k+=1
print()

