Calculate the even parity bit
RTK 06/2021

Read seven bits

+++++++[                    mem(0) = 7
    >,.                     mem(1) = input; echo
    --------------------
    --------------------
    --------                sub 48
    [                       inner loop if bit is one
        -                   subtract the bit from mem(1)
        >+                  look at mem(2); increment mem(2)
        <                   look at mem(1)
    ]                       exit loop because mem(1) is zero
    <-                      look at mem(0); decrement mem(0)
]                           loop if mem(0) not zero

subtract bit sum toggling parity bit
if parity bit is zero end at mem(2)
if parity bit is one end at mem(0)
regardless move to memory with proper value and print it

>>                          look at mem(2)
[                           loop if mem(2) not zero
    [                       if mem(2) not zero
        -                   subtract one
        >                   look at mem(3)
        +                   increment it
        >                   look at mem(4); which is zero
    ]                       do not loop
    <<                      look back to mem(2)
    [                       if mem(2) not zero
        -                   subtract one
        >                   look at mem(3)
        -                   decrement
        >                   look at mem(4); which is zero
    ]                       do not loop
    <<                      look at mem(2) or mem(0) if sum exhausted
]                           loop if not zero

print the parity bit

>>>                         look at mem(3) which is one or mem(5) which is zero
++++++++++++++++++++
++++++++++++++++++++
++++++++.                   add 48 and print
>                           look at the next location which is zero
++++++++++.                 set to 10 and print the newline

