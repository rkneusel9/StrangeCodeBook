#  Convert the values output by random.png into a file of doubles
#  for C-based randomness tests

import struct
v = [float(i[:-1])/4093.0 for i in open("random.txt")]
s = struct.pack('d'*len(v), *v)
with open("random.dat","wb") as f:
    f.write(s)

