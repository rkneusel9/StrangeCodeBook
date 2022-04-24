[#
#  file: mult2.b
#
#  Multiply two single-digit numbers.  This version prints
#  the two-digit result using esolang.org example code.
#
#  RTK, 06-Jun-2021
#  Last update:  06-Jun-2021
#
###############################################################]

get the first digit in mem(0)

,--------------------
--------------------
--------

print " * "

>++++++++++++++++
++++++++++++++++.
++++++++++.
----------.

get the second digit in mem(1)

,--------------------
--------------------
--------

multiply

<[-                 dec mem(0)
    >[-             look at mem(1); dec
        >+>+<<      inc mem(2); inc mem(3); look at mem(1)
    ]               continue until mem(1) is zero
    >[-<+>]         look at mem(2); copy back to mem(1)
    <<              look at mem(0)
]                   loop until mem(0) is zero

the product is now in mem(3); looking at mem(0)

print " = "

++++++++++++++++
++++++++++++++++.
+++++++++++++++
++++++++++++++.
---------------
--------------.

This code from esolang_org brainfuck algorithms:

>>>                 move to mem(3)

>[-]>[-]+>[-]+<                         // Set n and d to one to start loop
[                                       // Loop on 'n'
    >[-<-                               // On the first loop
        <<[->+>+<<]                     // Copy V into N (and Z)
        >[-<+>]>>                       // Restore V from Z
    ]
    ++++++++++>[-]+>[-]>[-]>[-]<<<<<    // Init for the division by 10
    [->-[>+>>]>[[-<+>]+>+>>]<<<<<]      // full division
    >>-[-<<+>>]                         // store remainder into n
    <[-]++++++++[-<++++++>]             // make it an ASCII digit; clear d
    >>[-<<+>>]                          // move quotient into d
    <<                                  // shuffle; new n is where d was and
                                        //   old n is a digit
    ]                                   // end loop when n is zero
<[.[-]<]                                // Move to were Z should be and
                                        // output the digits till we find Z
<                                       // Back to V

<++++++++++.        newline

