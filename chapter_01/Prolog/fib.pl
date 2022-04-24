/*
*  file:  fib.pl
*
*  Find the N-th Fibonacci number.
*
*  RTK, 14-Apr-2021
*  Last update:  14-Apr-2021
*
*/

/*  Base cases  */
fib(1,1).
fib(2,1).

/*  General rule  */
fib(N,F) :-
    N > 2,
    N1 is N-1,
    N2 is N-2,
    fib(N1,F1),
    fib(N2,F2),
    F is F1 + F2.

