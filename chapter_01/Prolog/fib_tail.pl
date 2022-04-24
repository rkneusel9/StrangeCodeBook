/*
*  file:  fib_tail.pl
*
*  Find the N-th Fibonacci number
*  (tail recursive)
*
*  RTK, 16-Apr-2021
*  Last update:  16-Apr-2021
*
*/

/*  Base case  */
fib(1,A,F,F).

/*  General rule  */
fib(N,A,B,F) :-
    N > 0,
    N1 is N-1,
    B1 is A+B,
    fib(N1,B,B1,F).

