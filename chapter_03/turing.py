#
#  file:  turing.py
#
#  Simulate a Turing machine.  Note, many simulators talk
#  about moving the tape.  In Turing's 1936 paper, he explains
#  the machine as moving the reader.  We follow that convention
#  so 'R' means 'read the square to the right' (i.e. move right)
#  which is equivalent to moving the tape to the left.
#
#  If implementing a program for a machine that moves the tape,
#  change all R's to L's and vice versa.
#
#  RTK, 30-Apr-2021
#  Last update:  05-May-2021
#
################################################################

import sys

#  Configuration table: (<state>, <symbol>, <write>, <move>, <new_state>)
#
#  Using the current state (C) and current symbol, find the table entry
#  that matches.  Do the write operation, do the move operation, and set the
#  state to the new state or end.  Repeat.

NAMES = [
    "Turing's first example",
    "change 0's to 1's",
    "unary increment: 111 -> 1111",
    "binary increment",
    "unary subtraction: 11111 111 -> 5 - 3",
]

PROGS = [
    ((0,' ','0','R',1),     #  Turing's first example
     (1,' ',' ','R',2),
     (2,' ','1','R',3),
     (3,' ',' ','R',0)),

    ((0,'0','1','R', 0),    #  change 0's to 1'
     (0,'1','1','R',-1),
     (0,' ',' ','L',-1)),

    ((0,'1','1','R', 0),    #  unary increment
     (0,'0','1','L',-1),
     (0,' ','1','L',-1)),

    ((0,' ',' ','L', 1),    #  add one to the binary number
     (0,'0','0','R', 0),    #  already on the tape
     (0,'1','1','R', 0),
     (1,' ','1','R', 2),
     (1,'0','1','L', 2),
     (1,'1','0','L', 1),
     (2,' ',' ','L',-1),
     (2,'0','0','R', 2),
     (2,'1','1','R', 2)),

    ((0,' ',' ','R', 1),    #  unary subtraction:
     (0,'0','0','R', 0),    #    1111 111  -> 4 - 3
     (0,'1','1','R', 0),
     (1,' ',' ','L', 2),
     (1,'0','0','R', 1),
     (1,'1','1','R', 1),
     (2,' ',' ','R', 4),
     (2,'0','0','L', 2),
     (2,'1','0','L', 3),
     (3,' ',' ','L', 7),
     (3,'0','0','L', 3),
     (3,'1','1','L', 3),
     (4,' ',' ','L', 5),
     (4,'0','0','R', 4),
     (4,'1','1','R', 4),
     (5,' ',' ','L', 6),
     (5,'0',' ','L', 5),
     (5,'1','1','L', 5),
     (6,' ',' ','R',-1),
     (6,'0',' ','L', 6),
     (6,'1','1','L', 6),
     (7,' ',' ','R',-1),
     (7,'0','0','L', 7),
     (7,'1','0','R', 0)),

    ((0,'0','1','R', 0),    #  two's-complement
     (0,'1','0','R', 0),
     (0,' ',' ','L', 1),
     (1,' ','1','R', 2),
     (1,'0','1','L', 2),
     (1,'1','0','L', 1),
     (2,' ',' ','L',-1),
     (2,'0','0','R', 2),
     (2,'1','1','R', 2)),
]


################################################################
#  TuringMachine
#
class TuringMachine:
    """Implement a Turing machine"""

    #-----------------------------------------------------------
    #  Step
    #
    def Step(self):
        """Do the current step and update the state"""

        #  Find the next instruction
        found = False
        for p in self.prog:
            if (p[0] == self.c) and (self.tape[self.tc] == p[1]):
                found = True
                break
        if (not found):
            raise ValueError("No match found for current state: (%d,'%s')" % (self.c,self.tape[self.tc]))

        #  Execute the instruction
        w,m,c = p[2:]
        if (w != ''):
            self.tape[self.tc] = w
        if (m == 'R'):
            self.tc += 1
        elif (m == 'L'):
            self.tc -= 1
        self.c = c


    #-----------------------------------------------------------
    #  Done
    #
    def Done(self):
        """Return true if the program is done"""

        if (self.c == -1) or (self.tc < 0) or (self.tc == self.M):
            return True  # end state or fell off the tape
        return False


    #-----------------------------------------------------------
    #  Run
    #
    def Run(self):
        """Run a program"""

        while (not self.Done()):
            if (self.trace):
                s = "".join(self.tape)
                t = " "*self.tc + "^"
                print("%s, (state=%d, tc=%d)" % (s,self.c,self.tc))            
                print("%s" % t)
                _ = input("?")
                if (_.lower() == "q"):
                    quit()
            self.Step()


    #-----------------------------------------------------------
    #  Result
    #
    def Result(self):
        """Display the tape and final state"""
        
        print()
        print("Program complete: (state=%d, tc=%d)" % (self.c, self.tc))
        print()
        print("[%s]" % "".join(self.tape))
        print()
        print("Program:")
        for p in self.prog:
            s,sym,w,m,c = p
            sym = "'"+sym+"'"
            w = '---' if (w == '') else "'"+w+"'"
            m = '---' if (m == '') else "'"+m+"'"
            print("    %2d, %s ==> %s, %s, %2d" % (s,sym,w,m,c))
        print()


    #-----------------------------------------------------------
    #  __init__
    #
    def __init__(self, prog, tape=None, M=100, trace=False):
        """Set up the machine"""

        if (tape is None):
            self.tape = [' ']*M
            self.M = M
        else:
            tape.append(' ')  # extra blank added
            self.tape = tape
            self.M = len(tape)

        self.c = 0          # start in state 0
        self.tc = 0         # start at position zero
        self.prog = prog    # state table, i.e. the program
        self.trace = trace  # trace or not


################################################################
#  main
#
def main():
    """Run a program"""

    if (len(sys.argv) == 1):
        print()
        print("turing <prog> [<M> | <list>] [-t]")
        print()
        print("  <prog> - program # [0,%d]" % (len(PROGS)-1,))
        print("  <M>    - blank tape of size M")
        print("  <list> - initial tape (list: 0,1,2=blank)")
        print("  <-t>   - trace, if present")
        print()
        print("programs:")
        for i in range(len(NAMES)):
            print("    %d: %s" % (i,NAMES[i]))
        print()
        return

    prog = PROGS[int(sys.argv[1])]
    trace = False

    if (len(sys.argv) > 2):
        tape = M = None
        try:
            M = int(sys.argv[2])
        except:
            tape = []
            for t in eval(sys.argv[2]):
                if (t is not 2):
                    tape.append(str(t))
                else:
                    tape.append(' ')
        if (len(sys.argv) > 3):
            trace = True
    else:
        tape = None
        M = 100

    tm = TuringMachine(prog, tape=tape, M=M, trace=trace)
    tm.Run()
    tm.Result()


if (__name__ == "__main__"):
    main()

