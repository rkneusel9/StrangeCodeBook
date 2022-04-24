REM
REM  Generate points to plot the Sierpinski triangle
REM
10 dim a(3),b(3)
15 a(0) = 140 : b(0) = 0 : a(1) = 0 : b(1) = 191 : a(2) = 279 : b(2) = 191
20 x = a(0) : y = b(0)
25 for i = 1 to 35000
30 n = rnd(3)
35 x = 0.5*(x+a(n)) : y = 0.5*(y+b(n))
40 print x, 191-y
45 next i
50 exit

