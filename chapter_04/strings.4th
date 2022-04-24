\
\  file:  strings.4th
\
\  Alternate string words
\
\  RTK, 03-Mar-2021
\  Last update:  03-Mar-2021
\
\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

\  Create a block of bytes initialized to zero
: variable$ ( n -- )
  create here here rot dup allot
  + swap do  0 i c!  loop
  does> ;

\  Display a null-terminated string
: disp ( addr -- )
  begin  
    dup c@ dup 0= 0=
  while
    emit 1+
  repeat
  drop drop ;

\  Input with null termination
: input ( addr len -- )
  over >r  accept  r> + 0 swap c! ;

\  String length
: strlen ( addr -- )
  0 begin 2dup + c@ 0= 0= while  1+  repeat  nip ;

\  Get a string and echo it
80 variable$ str

: main ( -- )
  ." Please enter your name: "
  str 80 input
  cr ." Hello there, " str disp cr ;

