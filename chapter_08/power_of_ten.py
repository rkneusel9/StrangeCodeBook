#
#  file:  power_of_ten.py
#
#  Report if the input is a power of ten and, if so, its exponent.
#
#  Pipe the output of primes10.frac to this program to see the progression
#  of 10**prime.
#
#  RTK, 05-Apr-2021
#  Last update:  05-Apr-2021
#  
################################################################

def isPowerOfTen(d):
    s = str(d)
    z = s.count("0")
    p = len(s)-1
    return ((s[0] == "1") and (z == p)), p

while (True):
    try:
        d = int(input())
    except:
        exit(0)
    ok, p = isPowerOfTen(d)
    if (ok):
        print("10**%d" % (p,), flush=True)

