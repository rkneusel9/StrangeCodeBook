\
\  file:  bubble.4th
\
\  Sort a random array
\
\  RTK, 03-Mar-2021
\  Last update:  05-Mar-2021
\
\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

( A pseudorandom generator -- Park and Miller )
variable seed  8675309 seed ! ( default seed )
: rand ( -- n ) 48271 seed @ * 2147483647 mod  dup seed ! ;
: random ( m -- n ) rand swap mod ;

( A word to create arrays )
: array ( n -- ) create cells allot
        ( -- a ) does> swap cells + ;

( Define an array )
100 constant M
M array A

( Fill the array with random values )
: randomize ( n -- )
   0 do  100 random  i A !  loop ;

( Display the array )
: show ( n -- )  0 do  i A @ . space  loop ;

( Swap two elements of the array )
: exchange ( i j -- ) 
  dup A @ >r swap dup A @ swap r> swap A ! swap A ! ;

( Bubble sort )
: bubble ( -- )
  M 0 do
    M 0 do
      i A @  j A @  > if  i j exchange  then
    loop
  loop ;

: main ( -- )  
  utime drop 2147483647 mod seed ! ( gforth )
  ." Unsorted: " cr
  M randomize
  M show cr
  bubble
  ." Sorted: " cr
  M show cr ;

main  bye

