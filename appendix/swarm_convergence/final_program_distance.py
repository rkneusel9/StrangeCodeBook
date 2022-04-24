#
#  file:  final_program_distance.py
#
#  RTK, 28-Jan-2021
#  Last update:  28-Jan-2021
#
################################################################

import numpy as np
import editdistance

prg = [i[:-1] for i in open("runs_10.txt")]
dist = []
for i in range(len(prg)):
    for j in range(len(prg)):
        if (i == j):
            continue
        dist.append(editdistance.eval(prg[i],prg[j]))
dist = np.array(dist) / len(prg[0])
print()
print("10-instructions: %0.4f +/- %0.4f" % (dist.mean(), dist.std(ddof=1)/np.sqrt(len(dist))))

prg = [i[:-1] for i in open("runs_60.txt")]
dist = []
for i in range(len(prg)):
    for j in range(len(prg)):
        if (i == j):
            continue
        dist.append(editdistance.eval(prg[i],prg[j]))
dist = np.array(dist) / len(prg[0])
print("60-instructions: %0.4f +/- %0.4f" % (dist.mean(), dist.std(ddof=1)/np.sqrt(len(dist))))
print()


