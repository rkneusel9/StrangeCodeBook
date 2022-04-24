[#
#  file: mult.b
#
#  Multiply two single-digit numbers with the product in mem(3)
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
++++++++++.         newline

