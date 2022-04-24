import sys

if (len(sys.argv) == 1):
    print("collatz <n>")
    exit(0)

def generate(x):
    m = -1
    s = 0
    while (x != 1):
        s += 1
        if (x % 2 == 0):
            x = x//2
        else:
            x = 3*x + 1
        if (x > m):
            m = x
    return m, s

n = int(sys.argv[1])
m,s = generate(n)
print("n=%d, max=%d, steps=%d" % (n,m,s))

