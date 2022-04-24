[#
#  file:  ones.b
#
#  Output the ones' complement of the input byte.
#
#  RTK, 06-Jun-2021
#  Last update:  06-Jun-2021
#
###############################################################]

Read eight bits

++++++++[
    ->              decrement mem(0); look at mem(1)

    >+<,            look at mem(2); inc; mem(1); input
    ----------
    ----------
    ----------
    ----------
    --------        sub 48
    [->-<]          if one then dec mem(2)
    >               look at mem(2)
    ++++++++++
    ++++++++++
    ++++++++++
    ++++++++++
    ++++++++.       add 48; print
    [-]<            zero mem(2); look at mem(1)

    <               look at mem(0)
]
++++++++++.         mem(0) = 10; print newline

