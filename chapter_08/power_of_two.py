#
#  file:  power_of_two.py
#
#  Report if the input is a power of two and, if so, its exponent.
#
#  Pipe the output of primes.frac to this program to see the progression
#  of 2**prime.
#
#  RTK, 22-Mar-2021
#  Last update:  22-Mar-2021
#  
################################################################

def isPowerOfTwo(d):
    s = "{0:b}".format(d)
    n = s.count("1")
    p = len(s)-1
    return (n == 1), p

while (True):
    try:
        d = int(input())
    except:
        exit(0)
    ok, p = isPowerOfTwo(d)
    if (ok):
        print("2**%d = %d" % (p, 2**p), flush=True)

