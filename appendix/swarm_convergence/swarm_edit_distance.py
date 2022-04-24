#
#  file:  swarm_edit_distance.py
#
#  Mean edit distance between best program
#  and initial and final swarms.
#
#  RTK, 27-Jan-2021
#  Last update:  29-Jan-2021
#
################################################################

import numpy as np
import editdistance

#  Program length 10
prg = [i[:-1] for i in open("swarm_10.txt")]
best = prg[0]
init = prg[1:31]
final= prg[31:]

i = []
for p in init:
    i.append(editdistance.eval(best, p))
i = np.array(i) / len(init[0])

f = []
for p in final:
    f.append(editdistance.eval(best, p))
f = np.array(f) / len(final[0])

print()
print("Program length 10: %0.3f initial, %0.3f final" % (i.mean(), f.mean()))

#  Program length 60
prg = [i[:-1] for i in open("swarm_60.txt")]
best = prg[0]
init = prg[1:31]
final= prg[31:]

i = []
for p in init:
    i.append(editdistance.eval(best, p))
i = np.array(i) / len(init[0])

f = []
for p in final:
    f.append(editdistance.eval(best, p))
f = np.array(f) / len(final[0])

print("Program length 60: %0.3f initial, %0.3f final" % (i.mean(), f.mean()))
print()

