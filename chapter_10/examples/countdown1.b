Count down from 9 to 0 with newlines
and print the digit as ASCII

++++++++++      mem(0) = 10
>               look at mem(1)
++++++++++      mem(1) = 10
[               enter loop if mem(1) not zero
 -              decrement mem(1)
 ++++++++++
 ++++++++++
 ++++++++++
 ++++++++++
 ++++++++       add 48
 .              print
 ----------
 ----------
 ----------
 ----------
 --------       sub 48
 <              look at mem(0)
 .              print it
 >              look at mem(1)
]               loop if mem(1) is not zero

