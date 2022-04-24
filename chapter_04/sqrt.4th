\
\  file: sqrt.4th
\
\  Integer square root by counting the number
\  of successive odd numbers that can be subtracted.
\
\  RTK, 03-Mar-2021
\  Last update:  06-Mar-2021
\
\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

: sqrt ( n -- sqrt[n] )
  0 >r 1 swap BEGIN 
    dup 0 > 
  WHILE 
    over - swap 1+ 1+ swap r> 1+ >r 
  REPEAT 2drop r> ;

: dsqr ( n -- sqrt[n], the brute force way )
  0 BEGIN  2dup dup * >  WHILE  1+  REPEAT nip ;

( Newton's method )
: step ( n xi -- n xi x_{i+1} )  2dup dup rot swap dup 0= if 2drop else / + then 2/ ;
: newton ( n -- sqr[n] )
  dup 2/ step BEGIN 2dup swap < WHILE nip step REPEAT drop nip ;

( Park and Miller PRNG )
variable seed  8675309 seed ! ( default seed )
: rand ( -- n ) 48271 seed @ * 2147483647 mod  dup seed ! ;
: random ( m -- n ) rand swap mod ;

( Time to find the square root by method )

variable x
utime drop dup seed ! x ! ( keep seed )

: run0 ( -- ) 100000 0 do  1000 random 1+ dup * sqrt   drop  loop ;
: run1 ( -- ) 100000 0 do  1000 random 1+ dup * dsqr   drop  loop ;
: run2 ( -- ) 100000 0 do  1000 random 1+ dup * newton drop  loop ;

: main ( -- )
  utime  run0  utime 2swap d- d. cr
  x @ seed !
  utime  run1  utime 2swap d- d. cr 
  x @ seed !
  utime  run2  utime 2swap d- d. cr ;

main  bye

