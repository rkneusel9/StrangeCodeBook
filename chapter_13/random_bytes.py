import numpy as np
d = np.loadtxt("numbers.txt")
b = []
for i in range(len(d)):
    b.append(int(np.floor(256*d[i])))
open("random.dat","wb").write(bytearray(b))

