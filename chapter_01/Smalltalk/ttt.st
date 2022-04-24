v := stdin nextLine asInteger.

(v < 0) ifTrue: [
    a:=-1
] ifFalse: [ 
    (v > 0) ifTrue: [
        a:=1
    ] ifFalse: [
        a:=0
    ]
].

a displayNl.

