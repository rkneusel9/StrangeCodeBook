#!/usr/bin/python3
#
#  file:  bedit.py
#
#  A simple Befunge-93 editor.  Public domain.
#
#  RTK, 14-Jun-2021
#  Last update:  04-Jan-2022
#
################################################################

import sys
import os
import curses

################################################################
#  BEdit
#
class BEdit:
    """A simple Befunge-93 editor"""

    #-----------------------------------------------------------
    #  ReadFile
    #
    def ReadFile(self):
        """Read the file"""

        self.text = [[" "]*80]*25
        lines = open(self.fname).read().split("\n")
        if (lines[-1] == ""):
            lines = lines[:-1]
        for i,line in enumerate(lines):
            t = self.text[i][:]
            for j,c in enumerate(line):
                t[j] = c
            self.text[i] = t[:]

    #-----------------------------------------------------------
    #  WriteFile
    #
    def WriteFile(self):
        """Write the file"""

        with open(self.fname,"w") as f:
            for i in range(25):
                f.write("%s\n" % ("".join(self.text[i])))
        self.modified = False


    #-----------------------------------------------------------
    #  PrintCommands
    #
    def PrintCommands(self):
        """Display the command reference"""

        s = [
            "Editor:",
            "    arrows, ^Write, ^Exit,",
            "    ^Horiz clear, ^Vert clear",
            "",
            "Befunge-93:",
            "    0-9    push number",
            "    +-*/%  ( a b -- a op b )",
            "    !      ( a -- !a )",
            "    `      ( a b -- a>b )",
            "    ><^v   set direction",
            "    ?      random direction",
            "    _      pop; 0=right, else left",
            "    |      pop; 0=down, else up",
            '    "      push string',
            "    :      ( a -- a a )",
            "    \      ( a b -- b a )",
            "    $      ( a -- )",
            "    .      pop; print as integer",
            "    ,      pop; print as char",
            "    #      skip next cell (bridge)",
            "    p      ( v c r -- ) play[r,c] = v",
            "    g      ( c r -- ) push play[r,c]",
            "    &      input number; push",
            "    ~      input char; push",
            "    @      exit program",
        ]

        for i,t in enumerate(s):
            self.screen.addstr(i,82,t, curses.color_pair(2))


    #-----------------------------------------------------------
    #  Status
    #
    def Status(self):
        """Create the status string"""

        status = "BEdit v1, file: %s" % self.fname
        if (self.modified):
            status += " (modified)"
        pos = "(%2d,%2d)" % (self.row,self.col)
        status += " "*(80 - len(status) - len(pos))
        status += pos
        return status


    #-----------------------------------------------------------
    #  DisplayScreen
    #
    def DisplayScreen(self):
        """Display the screen"""

        #  Show the text
        self.screen.clear()
        for i in range(25):
            self.screen.addstr(i,0, "".join(self.text[i]))
            self.screen.addstr(i,80," ", curses.color_pair(1))
        self.PrintCommands()
        self.screen.addstr(25,0, " "*81, curses.color_pair(1))
        self.screen.addstr(25,0, self.Status(), curses.color_pair(1))

        #  Highlight the cursor text
        ch = self.text[self.row][self.col]
        self.screen.addch(self.row, self.col, ch, curses.A_REVERSE)


    #-----------------------------------------------------------
    #  Process
    #
    def Process(self, ch):  
        """Process user action"""

        if (ch == 258):   #  down arrow
            self.row += 1
            self.dir = "down"
        elif (ch == 259): #  up arrow
            self.row -= 1
            self.dir = "up"
        elif (ch == 260): #  left arrow
            self.col -= 1
            self.dir = "left"
        elif (ch == 261): #  right arrow
            self.col += 1
            self.dir = "right"
        elif (ch == 23):  #  ctrl-w
            if (self.modified):
                self.WriteFile()
        elif (ch == 5):   #  ctrl-e
            if (self.modified):
                self.WriteFile()
            self.running = False
        elif (ch == 8):   #  ctrl-h
            for i in range(self.col,80):
                t = self.text[self.row][:]
                t[i] = " "
                self.text[self.row] = t[:]
            self.modified = True
        elif (ch == 22):  #  ctrl-v
            for i in range(self.row,25):
                t = self.text[i][:]
                t[self.col] = " "
                self.text[i] = t[:]
            self.modified = True
        elif (ch > 31) and (ch < 127):
            t = self.text[self.row][:]
            t[self.col] = chr(ch)
            self.text[self.row] = t[:]
            self.modified = True

            if (self.dir == "down"):
                self.row += 1
            elif (self.dir == "up"):
                self.row -= 1
            elif (self.dir == "left"):
                self.col -= 1
            else:
                self.col += 1

        #  Wrap as necessary
        self.row = 24 if (self.row < 0) else self.row
        self.row = 0 if (self.row > 24) else self.row
        self.col = 79 if (self.col < 0) else self.col
        self.col = 0 if (self.col > 79) else self.col


    #-----------------------------------------------------------
    #  Run
    #
    def Run(self):
        """Run the app"""

        #  Event loop
        while (self.running):
            self.DisplayScreen()
            self.Process(self.screen.getch())

        #  Exit
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()
        exit(0)


    #-----------------------------------------------------------
    #  __init__
    #
    def __init__(self):
        """Initialize the app"""

        self.text = [[" "]*80]*25
        self.fname = sys.argv[1]
        if (os.path.exists(self.fname)):
            self.ReadFile()
        self.row = self.col = 0
        self.running = True
        self.dir = "right"
        self.modified = False

        self.screen = curses.initscr()
        self.screen.keypad(1)
        curses.curs_set(0)
        curses.start_color()
        self.screen.clear()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)


################################################################
#  main
#
def main():
    """run the app"""

    if (len(sys.argv) == 1):
        print()
        print("bedit <file>")
        print()
        print("  <file>  -  File to edit. Create if new.")
        print()
        return

    try:
        BEdit().Run()
    except:
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()
        print()
        print("Unable to initialize the screen.  Minimum window size 120x26 required.")
        print()


if (__name__ == "__main__"):
    main()

