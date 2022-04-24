#
#  file:  hello.py
#
#  Polynomial fit for HELLO, WORLD!
#
#  RTK, 27-Dec-2020
#  Last update:  27-Dec-2020
#
################################################################

import numpy as np
import matplotlib.pylab as plt

def f(x,p):
    ans = 0.0
    for i in range(len(p)):
        ans += p[i]*x**(len(p)-1-i)
    return ans

def main():
    x = np.arange(13)
    y = np.array([72,69,76,76,79,44,32,87,79,82,76,68,33])
    p = np.polyfit(x,y,12)

    for i in range(len(x)):
        yf = f(x[i],p)
        print("Y:%d  YF:%0.3f" % (y[i],yf))

    print()
    for i in range(len(p)):
        print("X**%2d, P = %0.16e" % (len(p)-1-i,p[i]))
    print()

    xf = np.linspace(0,12,1000)
    yf = []
    for i in range(len(xf)):
        yf.append(f(xf[i],p))

    plt.plot(x,y, marker='o', linestyle='none', color='k')
    plt.plot(xf,yf, color='k')
    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.savefig("hello.png", dpi=300)
    plt.savefig("hello.eps", dpi=300)
    plt.show()


if (__name__ == "__main__"):
    main()

