#  Higher-order functions in Python

def runner(f,x):
    return f(x)

def thing1(x):
    return x*x

def thing2(x):
    return x*x*x

g = [thing1, thing2]

for i in range(1,10):
    for t in g:
        print("%5d" % runner(t,i), end="")
    print()

