#! /usr/bin/python

#
#  file:  pic0.py
#
#  A small language for 10F2xx devices
#
#  RTK, 13-Nov-2006
#  Last update:  31-Dec-2006
#
#  Remaining:
#       [*] finish IF, ELSE, THEN keywords
#       [*] store, fetch in memory range
#       [*] bit set, clear, read (number or equate in range)
#       [*] ensure that labels, equates are valid assembler labels
#       [*] '_' to increment argument position
#       [*] optimization
#       [*] standard macros - disable WDT, etc.
#       [*] equate alone leaves address in register
#       [*] system equates allowed, output as labels
#       [*] W -> R0, R0 -> W
#       [*] if(equ^3) and if(equ/3) style "if" statements
#       [*] assembly code inlined in a function
#       [*] added equ++ and equ-- statements
#       [*] no_sleep directive
#       [*] test all library routines
#       [*] documentation with examples
#
################################################################

#  Imports
import sys
from datetime import datetime
from string import *
from types import *


##############################################################
#
#  Assembly code for library words
#
piclib = {
    '+' :     ['L_plus',   ['','movf','R1,w'],          \
                           ['','addwf','R0,f']],
    '-' :     ['L_minus',  ['','movf','R1,w'],          \
                           ['','subwf','R0,f']],
    '=' :     ['L_equal',  ['','movf','R1,w'],          \
                           ['','subwf','R0,f'],         \
                           ['','goto','L_zequal']],
    '0=':     ['L_zequal', ['','movf','R0,w'],          \
                           ['','movwf','R1'],           \
                           ['','clrf','R0'],            \
                           ['','movf','R1,f'],          \
                           ['','btfsc','STATUS,Z'],     \
                           ['','incf','R0,f']],      
    '<<':     ['L_mult2',  ['','bcf','STATUS,C'],       \
                           ['','rlf','R0,f']],
    '>>':     ['L_div2',   ['','bcf','STATUS,C'],       \
                           ['','rrf','R0,f']],
    '<<<':    ['L_rotp',   ['','rlf','R0,f']],
    '>>>':    ['L_rotn',   ['','rrf','R0,f']],
    'and':    ['L_and',    ['','movf','R1,w'],          \
                           ['','andwf','R0,f']],
    'or' :    ['L_or',     ['','movf','R1,w'],          \
                           ['','iorwf','R0,f']],
    'xor':    ['L_xor',    ['','movf','R1,w'],          \
                           ['','xorwf','R0,f']],
    '~' :     ['L_comp',   ['','comf','R0,f']],
    'sleep':  ['L_sleep',  ['','sleep','']],
    'option': ['L_option', ['','option','']],
    'tris':   ['L_tris',   ['','tris','GPIO']],
    'clrwdt': ['L_clrwdt', ['','clrwdt','']],
    'swapn':  ['L_swapn',  ['','swap','R0,f']],
    '1+' :    ['L_1plus',  ['','incf','R0,f']],
    '1-' :    ['L_1minus', ['','decf','R0,f']],
    '2+' :    ['L_2plus',  ['','incf','R0,f'],          \
                           ['','incf','R0,f']],
    '2-' :    ['L_2minus', ['','decf','R0,f'],          \
                           ['','decf','R0,f']],
    '>' :     ['L_ungt',   ['','movf','R0,w'],          \
                           ['','subwf','R1,f'],         \
                           ['','clrf','R0'],            \
                           ['','btfss','R1,7'],         \
                           ['','retlw','0'],            \
                           ['','incf','R0,f'],          \
                           ['','retlw','0']],
    '<' :     ['L_unlt',   ['','movf','R0,w'],          \
                           ['','subwf','R1,f'],         \
                           ['','btfsc','STATUS,Z'],     \
                           ['','goto','L_unlt0'],       \
                           ['','clrf','R0'],            \
                           ['','btfsc','R1,7'],         \
                           ['','retlw','0'],            \
                           ['','incf','R0,f'],          \
                           ['','retlw','0'],            \
                           ['L_unlt0','clrf','R0']],
    'W->R0' : ['L_W_RO',   ['','movwf','R0']],
    'R0->W' : ['L_R0_W',   ['','movf','R0,w']],
}    

#
#  Initial symbol table.  Copied to internal symbol table on compiler init.
#
#  Types:
#      'equ' : equate to a number     (value is number)
#      'lib' : library routine        
#              value is subroutine vs inline cutoff, -1 => always subroutine, 0 = always inline
#              a third value is the name of a dependency that must be included as well
#      'usr' : user defined routine
#      'kwd' : reserved keyword
#
symtable = {
    '+'        : ['lib',  3],
    '-'        : ['lib',  3],
    '='        : ['lib', -1, '0='],
    '0='       : ['lib', -1],
    '<<'       : ['lib',  3],
    '>>'       : ['lib',  3],
    '<<<'      : ['lib',  0],
    '>>>'      : ['lib',  0],
    'and'      : ['lib',  3],
    'or'       : ['lib',  3],
    'xor'      : ['lib',  3],
    '~'        : ['lib',  0],
    'sleep'    : ['lib',  0],
    'option'   : ['lib',  0],
    'tris'     : ['lib',  0],
    'clrwdt'   : ['lib',  0],
    'swapn'    : ['lib',  0],
    '1+'       : ['lib',  0],
    '1-'       : ['lib',  0],
    '2+'       : ['lib',  3],
    '2-'       : ['lib',  3],
    '>'        : ['lib', -1],
    '<'        : ['lib', -1],
    'W->R0'    : ['lib',  0],
    'R0->W'    : ['lib',  0],
    
    '{'        : ['kwd'],
    '}'        : ['kwd'],
    '['        : ['kwd'],
    ']'        : ['kwd'],
    'if'       : ['kwd'],
    '0if'      : ['kwd'],
    'else'     : ['kwd'],
    'then'     : ['kwd'],
    'break'    : ['kwd'],
    'cont'     : ['kwd'],
    '?break'   : ['kwd'],
    '?cont'    : ['kwd'],
    '?0break'  : ['kwd'],
    '?0cont'   : ['kwd'],

    'MCLRE_ON' : ['config', []],
    'MCLRE_OFF': ['config', []],
    'CP_ON'    : ['config', []],
    'CP_OFF'   : ['config', []],
    'WDT_ON'   : ['config', []],
    'WDT_OFF'  : ['config', []],
    'IntRC_OSC': ['config', []],
    'MCPU_ON'  : ['config', ['P10F220','P10F222']],
    'MCPU_OFF' : ['config', ['P10F220','P10F222']],
    'IOFSCS_8MHZ' : ['config', ['P10F220','P10F222']],
    'IOFSCS_4MHZ' : ['config', ['P10F220','P10F222']],

    #  Equates - these are output as numbers
    'GP3'      : ['equ', "d'3'"],
    'GP2'      : ['equ', "d'2'"],
    'GP1'      : ['equ', "d'1'"],
    'GP0'      : ['equ', "d'0'"],

    #  System equates - these are output as strings since the include files
    #                   for the assembler already know the proper value of these for
    #                   each processor type
    'INDF'        : ['equ', 'INDF'],
    'TMR0'        : ['equ', 'TMR0'],
    'PCL'         : ['equ', 'PCL'],
    'STATUS'      : ['equ', 'STATUS'],
    'FSR'         : ['equ', 'FSR'],
    'OSCCAL'      : ['equ', 'OSCCAL'],
    'GPIO'        : ['equ', 'GPIO'],
    'CMCON0'      : ['equ', 'CMCON0'],
    'CMPOUT'      : ['equ', 'CMPOUT'],
    'NOT_COUTEN'  : ['equ', 'NOT_COUTEN'],
    'POL'         : ['equ', 'POL'],
    'NOT_CMPT0CS' : ['equ', 'NOT_CMPT0CS'],
    'CMPON'       : ['equ', 'CMPON'],
    'CNREF'       : ['equ', 'CNREF'],
    'CPREF'       : ['equ', 'CPREF'],
    'NOT_CWU'     : ['equ', 'NOT_CWU'],
    'ADCON0'      : ['equ', 'ADCON0'],
    'ADRES'       : ['equ', 'ADRES'],			     
    'ANS1'        : ['equ', 'ANS1'],
    'ANS0'        : ['equ', 'ANS0'],
    'CHS1'        : ['equ', 'CHS1'],
    'CHS0'        : ['equ', 'CHS0'],
    'GO'          : ['equ', 'GO'],
    'NOT_DONE'    : ['equ', 'NOT_DONE'],
    'ADON'        : ['equ', 'ADON'],
    'ADRES7'      : ['equ', 'ADRES7'],
    'ADRES6'      : ['equ', 'ADRES6'],
    'ADRES5'      : ['equ', 'ADRES5'],
    'ADRES4'      : ['equ', 'ADRES4'],
    'ADRES3'      : ['equ', 'ADRES3'],
    'ADRES2'      : ['equ', 'ADRES2'],
    'ADRES1'      : ['equ', 'ADRES1'],
    'ADRES0'      : ['equ', 'ADRES0'],
    'GPWUF'       : ['equ', 'GPWUF'],
    'NOT_TO'      : ['equ', 'NOT_TO'],
    'NOT_PD'      : ['equ', 'NOT_PD'],
    'Z'           : ['equ', 'Z'],
    'DC'          : ['equ', 'DC'],
    'C'           : ['equ', 'C'],
    'NOT_GPWU'    : ['equ', 'NOT_GPWU'],
    'NOT_GPPU'    : ['equ', 'NOT_GPPU'],
    'T0CS'        : ['equ', 'T0CS'],
    'T0SE'        : ['equ', 'T0SE'],
    'PSA'         : ['equ', 'PSA'],
    'PS2'         : ['equ', 'PS2'],
    'PS1'         : ['equ', 'PS1'],
    'PS0'         : ['equ', 'PS0'],
    'CAL6'        : ['equ', 'CAL6'],
    'CAL5'        : ['equ', 'CAL5'],
    'CAL4'        : ['equ', 'CAL4'],
    'CAL3'        : ['equ', 'CAL3'],
    'CAL2'        : ['equ', 'CAL2'],
    'CAL1'        : ['equ', 'CAL1'],
    'CAL0'        : ['equ', 'CAL0'],
    'FOSC4'       : ['equ', 'FOSC4'],
}

#
#  Valid command names, for asm{ ... } output
#
cmds = ["addwf","andwf","clrf","clrw","comf","decf","decfsz","incf","incfsz","iorwf","movf","movwf",   \
        "nop","rlf","rrf","subwf","swapf","xorwf","bcf","bsf","btfsc","btfss","andlw","call","clrwdt", \
        "goto","iorlw","movlw","option","retlw","sleep","tris","xorlw"]


############################################################
#  Class PIC0Compiler
#
#
class PIC0Compiler(object):
    """A compiler for the PIC0 language."""
    
    
    ########################################################
    #  __init__
    #
    def __init__(self, src='', dest='', flags=''):
        """Set up a new compiler object."""
        
        #  Local copy of symbol table (see pic0lib.py)
        self.sym = symtable

        #  Set the instance vars
        self.src = src
        self.dest = dest
        self.flags = flags

        #  Pragmas
        self.no_sleep = False

        #  Version
        self.version = '1.0'


    #######################################################
    #  MakeNumber
    #
    def MakeNumber(self, s):
        """Make a number of a string, must be in range 0..255"""

        n = None
        if (s.count('x') != 0) or (s.count('X') != 0):
            try:
                n = atoi(s[2:], 16)
            except:
                pass
        elif (s.count('b') != 0) or (s.count('B') != 0):
            try:
                n = atoi(s[2:], 2)
            except:
                pass
        else:
            try:
                n = atoi(s, 10)
            except:
                pass

        if (n != None):
            if (n < 0) or (n > 255):
                return None
        return n
    

    ########################################################
    #  MakeDictionary
    #
    def MakeDictionary(self, typ):
        """Return a dictionary with all symbol table entries of typ"""

        d = {}
        for s in self.sym.keys():
            if self.sym[s][0] == typ:
                d[s] = self.sym[s][1:]
        return d
    
        
    ########################################################
    #  ParseSourceCode
    #
    def ParseSourceCode(self):
        """Parse the source code removing comments and separating into tokens."""

        #  Read the input file
        try:
            f = file(self.src, "r")
            s = f.read()
            f.close()
        except:
            print "\nUnable to load the source file: %s" % self.src
            sys.exit(1)

        #  Remove all comments
        comment = False
        w = ''
        for c in s:
            if (c==';') and (not comment):
                comment = True
            elif (comment) and (c=='\n'):
                comment = False
            elif (not comment):
                w += c
        
        #  Split into individual tokens
        self.tokens = w.split()
        

    #######################################################
    #  DetermineProcessor
    #
    def DetermineProcessor(self):
        """Identify the target processor."""

        self.processor = 'P10F200'
        for t in self.tokens:
            if t.upper() in ['P10F200','P10F202','P10F204','P10F206','P10F220','P10F222']:
                self.processor = t.upper()
                return


    #######################################################
    #  ReadPragmas
    #
    def ReadPragmas(self):
        """Identify any compiler directives."""

        for t in self.tokens:
            if t == "no_sleep":
                self.no_sleep = True
            #  others here...
            

    #######################################################
    #  ReadConfig
    #
    def ReadConfig(self):
        """Read any config settings."""

        self.config = []
        d = self.MakeDictionary('config')
        for t in self.tokens:
            if d.has_key(t):
                if d[t][0] == []:
                    self.config.append(t)
                else:
                    if self.processor in d[t][0]:
                        self.config.append(t)
                    else:
                        print "\nConfig not allowed with this processor: %s, %s" % (t, self.processor)
                        sys.exit(1)
            

    #######################################################
    #  SetupLibraryRoutines
    #
    def SetupLibraryRoutines(self):
        """Locate the library routines used."""

        #  Dictionary of used library routines and frequency of use
        freq = {}
        for t in self.tokens:
            if self.sym.has_key(t):
                if self.sym[t][0] == 'lib':
                    if freq.has_key(t):
                        freq[t] = freq[t]+1
                    else:
                        freq[t] = 1

        #  Check for dependencies
        if freq.has_key("="):
            freq["0="] = 1  # always subroutines

        #  Change these into a flag indicating subroutine (True) or inline (False)
        self.routines = {}
        for t in freq.keys():
            if self.sym[t][1] == -1:
                self.routines[t] = True
            elif self.sym[t][1] == 0:
                self.routines[t] = False
            elif freq[t] >= self.sym[t][1]:
                self.routines[t] = True
            else:
                self.routines[t] = False


    #######################################################
    #  ValidEquateName
    #
    def ValidEquateName(self, s):
        """Return true if argument is a valid equate label."""

        #  Name must start with a letter
        if s[0] not in ascii_letters:
            return False

        #  Additional characters must be letters, digits, or "_"
        w = ascii_letters + "_" + digits
        for i in s:
            if i not in w:
                return False

        return True
    

    #######################################################
    #  IdentifyEquates
    #
    def IdentifyEquates(self):
        """Locate all equates."""

        #  Add R0 and R1, location depends upon the processor
        if self.processor in ["P10F200","P10F204","P10F220"]:
            self.sym['R0'] = ['equ', "d'16'"]
            self.sym['R1'] = ['equ', "d'17'"]
        elif self.processor in ["P10F202","P10F206"]:
            self.sym['R0'] = ['equ', "d'8'"]
            self.sym['R1'] = ['equ', "d'9'"]
        elif self.processor == "P10F222":
            self.sym['R0'] = ['equ', "d'9'"]
            self.sym['R1'] = ['equ',"d'10'"]
        
        i = 0
        while i < len(self.tokens):
            t = self.tokens[i]
            if t == 'equ[':
                i += 1  #  next token
                while i < len(self.tokens)-1:
                    t0 = self.tokens[i]
                    t1 = self.tokens[i+1]
                    if t0 == ']':
                        break
                    else:
                        if not self.ValidEquateName(t0):
                            print "\nIllegal equate name: %s" % t0
                            sys.exit(1)
                        n = self.MakeNumber(t1)
                        if n == None:
                            print "\nNot a valid number: %s" % t1
                            sys.exit(1)
                        if self.sym.has_key(t0):
                            print "\nDuplicate equate: %s" % t0
                            sys.exit(1)
                        self.sym[t0] = ['equ', "d'%d'" % n]
                    i += 2
            i += 1
            
    
    #######################################################
    #  LocateFunctions
    #
    def LocateFunctions(self):
        """Locate all functions."""

        i = 0
        while i < len(self.tokens):
            t = self.tokens[i]
            if t == '[':
                i += 1  #  next token is name
                f = self.tokens[i]
                i += 1
                w = []
                while i < len(self.tokens)-1:
                    t = self.tokens[i]
                    if t == ']':
                        break
                    else:
                        w.append(t)
                    i += 1
                #  Put in the symbol table
                if self.sym.has_key(f):
                    print "\nDuplicate function name: %s" % f
                    sys.exit(1)
                self.sym[f] = ['user'] + w
            i += 1


    #######################################################
    #  IncrementRegister
    #
    def IncrementRegister(self):
        """Switch to the next register."""

        if self.reg == "R0":
            self.reg = "R1"
        else:
            self.reg = "R0"


    #######################################################
    #  GetLabel
    #
    def GetLabel(self):
        """Generate a new label."""

        s = "A_%04d" % self.labelNum
        self.labelNum += 1
        return s


    #######################################################
    #  CompileKeyword
    #
    def CompileKeyword(self, kwd):
        """Compile a keyword."""

        if kwd == "{":
            t = self.GetLabel()
            self.fcode.append([t,"",""])
            self.loop.append([t, self.GetLabel()])
        elif kwd == "}":
            if self.loop == []:
                print "\nLoop underflow!"
                sys.exit(1)
            t = self.loop[-1]
            self.loop = self.loop[0:-1]
            self.fcode.append(["","goto",t[0]])
            self.fcode.append([t[1],"",""])
        elif kwd == "break":
            t = self.loop[-1]
            self.fcode.append(["","goto",t[1]])
        elif kwd == "cont":
            t = self.loop[-1]
            self.fcode.append(["","goto",t[0]])
        elif kwd == "?break":
            t = self.loop[-1]
            q = self.GetLabel()
            self.fcode.append(["","movf","R0,f"])
            self.fcode.append(["","btfsc","STATUS,Z"])
            self.fcode.append(["","goto",q])
            self.fcode.append(["","goto",t[1]])
            self.fcode.append([q,"",""])
        elif kwd == "?0break":
            t = self.loop[-1]
            q = self.GetLabel()
            self.fcode.append(["","movf","R0,f"])
            self.fcode.append(["","btfss","STATUS,Z"])
            self.fcode.append(["","goto",q])
            self.fcode.append(["","goto",t[1]])
            self.fcode.append([q,"",""])
        elif kwd == "?cont":
            t = self.loop[-1]
            q = self.GetLabel()
            self.fcode.append(["","movf","R0,f"])
            self.fcode.append(["","btfsc","STATUS,Z"])
            self.fcode.append(["","goto",q])
            self.fcode.append(["","goto",t[0]])
            self.fcode.append([q,"",""])
        elif kwd == "?0cont":
            t = self.loop[-1]
            q = self.GetLabel()
            self.fcode.append(["","movf","R0,f"])
            self.fcode.append(["","btfss","STATUS,Z"])
            self.fcode.append(["","goto",q])
            self.fcode.append(["","goto",t[0]])
            self.fcode.append([q,"",""])
        elif kwd == "if":
            t_else = self.GetLabel()
            t_then = self.GetLabel()
            self.compare.append([t_else, t_then, False])
            self.fcode.append(["","decfsz","R0,w"])
            self.fcode.append(["","goto",t_else])
        elif kwd == "0if":
            t_else = self.GetLabel()
            t_then = self.GetLabel()
            self.compare.append([t_else, t_then, False])
            self.fcode.append(["","movf","R0,f"])
            self.fcode.append(["","btfss","STATUS,Z"])
            self.fcode.append(["","goto",t_else])
        elif kwd == "else":
            self.compare[-1][2] = True
            t_else, t_then, flag = self.compare[-1]
            self.fcode.append(["","goto",t_then])
            self.fcode.append([t_else,"",""])
        elif kwd == "then":
            if self.compare == []:
                print "\nCompare underflow!"
                sys.exit(1)
            t_else, t_then, flag = self.compare[-1]
            self.compare = self.compare[0:-1]
            if not flag:
                self.fcode.append([t_else,"",""])
            else:
                self.fcode.append([t_then,"",""])
        else:
            print "\nUnknown keyword: %s" % kwd
            sys.exit(1)


    #######################################################
    #  EquateInMemory
    #
    def EquateInMemory(self, s):
        """Return true if the equate value is in valid RAM."""

        #  If equate has a given value, proceed, otherwise
        #  let it be an assemble time error
        if len(s) <= 3:
            return True
        try:
            n = int(s[2:-1])
        except:
            return True

        if self.processor in ["P10F200","P10F204","P10F220"]:
            return (n >= 0x10) and (n <= 0x1F)
        elif self.processor in ["P10F202","P10F206"]:
            return (n >= 0x08) and (n <= 0x1F)
        elif self.processor == "P10F222":
            return (n >= 0x09) and (n <= 0x1F)
        else:
            return False


    #######################################################
    #  BitValid
    #
    def BitValid(self, loc, bit, equ):
        """Validate the equate and bit value."""

        if not equ.has_key(loc):
            print "\nUnknown equate in bit operation: %s" % loc
            sys.exit(1)
        if not self.EquateInMemory(equ[loc][0]):
            print "\nEquate not in RAM: %s" % loc
            sys.exit(1)     

        #  Ensure that the bit postion is valid
        if equ.has_key(bit):
            b = equ[bit]
        else:
            try:
                b = int(bit)
            except:
                print "\nBit position must be an equate or an integer, [0,7]"
                sys.exit(1)
        if (b < 0) or (b > 7):
            print "\nBit position must be in the range [0,7]"
            sys.exit(1)

        return b


    #######################################################
    #  CompileIfTest
    #
    def CompileIfTest(self, s, equ):
        """Compile an if(...) statement."""

        w = s[3:-1]
        if w.count("^") != 0:
            loc, bit = w.split("^")
            b = self.BitValid(loc, bit, equ)
            t_else = self.GetLabel()
            t_then = self.GetLabel()
            self.compare.append([t_else, t_then, False])
            self.fcode.append(["","btfss", "%s,%d" % (loc,b)])
            self.fcode.append(["","goto",t_else])
        elif w.count("/") != 0:
            loc, bit = w.split("/")
            b = self.BitValid(loc, bit, equ)
            t_else = self.GetLabel()
            t_then = self.GetLabel()
            self.compare.append([t_else, t_then, False])
            self.fcode.append(["","btfsc", "%s,%d" % (loc,b)])
            self.fcode.append(["","goto",t_else])
        else:
            print "\nIllegal bit test if statement: %s" % w
            sys.exit(1)


    #######################################################
    #  GetBitValue
    #
    def GetBitValue(self, s):
        """Return the value of the arg or -1 if not in range."""

        if type(s) is IntType:
            n = int(s)
            if (n<0) or (n>7):
                return -1
            return n

        if type(s) is StringType:
            d = self.MakeDictionary('equ')
            if not d.has_key(s):
                return -1
            n = d[s][1]
            if (n<0) or (n>7):
                return -1
            return n
        
        return -1


    #######################################################
    #  BitReference
    #
    def BitReference(self, t, equ):
        """Compile a bit reference."""

        #  Split and ensure that the argument are valid
        loc, bit = t.split(".")
        b = self.BitValid(loc, bit, equ)

        #  Output the code
        self.fcode.append(['','clrf','R0'])
        self.fcode.append(['','btfsc','%s,%d' % (loc,b)])
        self.fcode.append(['','incf','R0,f'])
    

    #######################################################
    #  BitSet
    #
    def BitSet(self, t, equ):
        """Compile a bit set operation."""

        #  Split and ensure that the arguments are valid
        loc, bit = t.split("^")
        b = self.BitValid(loc, bit, equ)

        #  Output the code
        self.fcode.append(['','bsf','%s,%d' % (loc,b)])
    

    #######################################################
    #  BitClear
    #
    def BitClear(self, t, equ):
        """Compile a bit clear operation."""

        #  Split and ensure that the arguments are valid
        loc, bit = t.split("/")
        b = self.BitValid(loc, bit, equ)

        #  Output the code
        self.fcode.append(['','bcf','%s,%d' % (loc,b)])


    #######################################################
    #  IncrementEquate
    #
    def IncrementEquate(self, t, equ):
        """Compile an increment statement."""

        s = t[0:-2]
        if not equ.has_key(s):
            print "\nUnknown equate in increment operation: %s" % s
            sys.exit(1)
        if not self.EquateInMemory(equ[s][0]):
            print "\nEquate not in RAM: %s" % s
            sys.exit(1)

        self.fcode.append(["","incf","%s,f" % (equ[s][0],)])
    

    #######################################################
    #  DecrementEquate
    #
    def DecrementEquate(self, t, equ):
        """Compile a decrement statement."""

        s = t[0:-2]
        if not equ.has_key(s):
            print "\nUnknown equate in decrement operation: %s" % s
            sys.exit(1)
        if not self.EquateInMemory(equ[s][0]):
            print "\nEquate not in RAM: %s" % s
            sys.exit(1)

        self.fcode.append(["","decf","%s,f" % (equ[s][0],)])
    

    #######################################################
    #  CompileFunction
    #
    def CompileFunction(self, label, src):
        """Compile a function."""

        #  Add the function name
        self.fcode.append([label,"",""])

        #  Reset keyword stacks
        self.loop = []
        self.compare = []

        #  Keep a dictionary of equates around
        dequ = self.MakeDictionary('equ')

        #  Compile each token in src
        wasNum = False
        i = 0
        while (i < len(src)):
            t = src[i]
            
            n = self.MakeNumber(t)
            if n != None:
                #  Compile a number
                if wasNum:
                    self.IncrementRegister()
                self.fcode.append(["","movlw","d'%d'" % n])
                self.fcode.append(["","movwf",self.reg])
                wasNum = True
            elif t == "_":
                if wasNum:
                    self.IncrementRegister()
                wasNum = True
            elif t == "asm{":
                asm = []
                i += 1
                while (i < len(src)) and (src[i] != "}"):
                    asm.append(src[i])
                    i += 1
                #  output the asm list
                s = ""
                first = True
                for w in asm:
                    if w == "\\":
                        self.fcode.append([s,"asm",""])
                        s = ""
                        first = True
                    else:
                        if first:
                            if w.lower() in cmds:
                                s = "\t"
                            first = False
                        s += w+" "
                if s != "":
                    self.fcode.append([s,"asm",""])
            elif len(t) > 3 and t[0:3] == "if(" and t[-1] == ")":
                self.CompileIfTest(t, dequ)
            elif t.count(".") != 0:
                self.BitReference(t, dequ)      #  bit reference
            elif t.count("^") != 0:
                self.BitSet(t, dequ)            #  bit set
            elif t.count("/") != 0:
                self.BitClear(t, dequ)          #  bit clear
            elif t.count("--") != 0:
                self.DecrementEquate(t, dequ)   #  decrement equate
            elif t.count("++") != 0:
                self.IncrementEquate(t, dequ)   #  increment equate
            else:  
                #  Handle ! and @
                store = fetch = False
                if t[-1] == "@":
                    s = t[0:-1]
                    fetch = True
                elif t[-1] == "!":
                    s = t[0:-1]
                    store = True
                else:
                    s = t

                #  Process according to symbol table entry
                if not self.sym.has_key(s):
                    print "\nUnknown token: %s" % s
                    sys.exit(1)
                    
                typ = self.sym[s][0]

                #  Library routine
                if typ == "lib":
                    if self.routines[s]:
                        #  Subroutine call
                        self.fcode.append(["","call",piclib[s][0]])
                    else:
                        #  Inlined code
                        for b in piclib[s][1:]:
                            self.fcode.append(b)
                    wasNum = False
                    self.reg = "R0"

                #  User-defined function call
                elif typ == "user":
                    self.fcode.append(["","call",s])
                    wasNum = False
                    self.reg = "R0"

                #  Keyword
                elif typ == "kwd":
                    self.CompileKeyword(s)
                    wasNum = False
                    self.reg = "R0"

                #  Equate reference
                elif typ == "equ":
                    if fetch:
                        if wasNum:
                            self.IncrementRegister()
                        equ = self.sym[s][1]
                        if not self.EquateInMemory(equ):
                            print "\nFETCH: Equate value outside memory range: %s" % s
                            sys.exit(1)
                        self.fcode.append(["","movf","%s,w" % equ])
                        self.fcode.append(["","movwf",self.reg])
                        wasNum = True
                    if store:
                        equ = self.sym[s][1]
                        if not self.EquateInMemory(equ):
                            print "\nSTORE: Equate value outside memory range: %s" % s
                            sys.exit(1)
                        self.fcode.append(["","movf","R0,w"])
                        self.fcode.append(["","movwf","%s" % equ])
                        wasNum = False
                    if (not fetch) and (not store):
                        if wasNum:
                            self.IncrementRegister()
                        equ = self.sym[s][1]
                        self.fcode.append(["","movlw","%s" % equ])
                        self.fcode.append(["","movwf",self.reg])
                        wasNum = True

                #  Unknown type
                else:
                    print "\nUnknown symbol table entry: %s" % repr(self.sym[s])
                    sys.exit(1)
            i += 1

        #  Add return if this isn't main
        if label != "main":
            self.fcode.append(["","retlw","0"])
        else:
            if not self.no_sleep:
                self.fcode.append(["","sleep",""])
        

    #######################################################
    #  CompileFunctions
    #
    def CompileFunctions(self):
        """Compile the functions and return the code."""

        self.labelNum = 0
        self.reg = "R0"
        func = self.MakeDictionary('user')
        self.fcode = []
        self.CompileFunction('main', func['main'])
        for f in func.keys():
            if f != 'main':
                self.CompileFunction(f, func[f])
        
    
    #######################################################
    #  GenerateCode
    #
    def GenerateCode(self):
        """Generate first-pass source code."""

        #  Check for a main function
        if not self.sym.has_key('main'):
            print "\nNo main function defined!"
            sys.exit(1)

        #  Code for functions
        self.CompileFunctions()

        #  Set up equates
        eq = self.MakeDictionary('equ')
        self.equ = []
        w = eq.keys()
        w.sort()
        for t in w:
            v = eq[t][0]
            if len(v) > 3:
                n = self.MakeNumber(v[2:-1])
                if n != None:
                    self.equ.append([t,'equ',"d'%d'" % n])
            
        #  Code for the library routines output as subroutines
        self.libcode = []
        for t in self.routines.keys():
            if self.routines[t]:
                p = piclib[t]
                l = p[0]      #  label
                p[1][0] = l   #  place in 1st instruction
                for i in p[1:]:
                    self.libcode.append(i)
                if t != "=":
                    self.libcode.append(["","retlw","0"])
    

    #######################################################
    #  MatchOp1
    #
    def MatchOp1(self, i, m):
        """See if the next four instructions match optimization 1."""
        
        if (i >= (m-4)):
            return False
        
        inst0 = self.fcode[i  ][1:]
        inst1 = self.fcode[i+1][1:]
        inst2 = self.fcode[i+2][1:]
        inst3 = self.fcode[i+3][1:]

        if (inst0[0] != 'movlw') or  \
           (inst1[0] != 'movwf') or  \
           (inst2[0] != 'movf')  or  \
           (inst3[0] != 'movwf') or  \
           (inst1[1] != 'R0')    or  \
           (inst2[1] != 'R0,w'):
            return False

        return True
    
    
    #######################################################
    #  MatchOp2
    #
    def MatchOp2(self, i, m):
        """See if the next four instructions match optimization 2."""

        if (i >= (m-4)):
            return False
        
        inst0 = self.fcode[i  ][1:]
        inst1 = self.fcode[i+1][1:]
        inst2 = self.fcode[i+2][1:]
        inst3 = self.fcode[i+3][1:]

        if (inst0[0] != 'movf')  or  \
           (inst1[0] != 'movwf') or  \
           (inst2[0] != 'movf')  or  \
           (inst3[0] != 'movwf'):
            return False

        t = inst1[1]
        s = inst2[1]
        if len(s) <= len(t):
            return False
        if t != s[0:-2]:
            return False

        return True


    #######################################################
    #  CodeOptimization
    #
    def CodeOptimization(self):
        """Optimize the code."""

        #  Search for "123 var!" optimizations
        i = 0
        t = []
        m = len(self.fcode)
        while (i < m):
            if self.MatchOp1(i,m):
                t.append(self.fcode[i])
                t.append(self.fcode[i+3])
                i += 3  # note extra i += 1 at end of loop
            else:
                t.append(self.fcode[i])
            i += 1
        self.fcode = t

        #  Search for "var! var@" optimizations
        i = 0
        t = []
        m = len(self.fcode)
        while (i < m):
            if self.MatchOp2(i,m):
                t.append(self.fcode[i])
                t.append(self.fcode[i+1])
                i += 3  # note extra i += 1 at end of loop
            else:
                t.append(self.fcode[i])
            i += 1
        self.fcode = t

        #  Assemble in order
        self.code = self.equ + self.fcode + self.libcode


    #######################################################
    #  OutputAsmFile
    #
    def OutputAsmFile(self):
        """Output the .asm file."""

        #  Open the output file
        try:
            f = file(self.dest, "w")
        except:
            print "\nUnable to open the output file: %s" % self.dest
            sys.exit(1)

        #  Header
        f.write(";\n")
        f.write(";  Generated by PIC0 compiler, version %s\n" % self.version)
        f.write(";  %s\n" % datetime.today().ctime())
        f.write(";\n")
        f.write("\n")
        f.write("\tprocessor\t%s\n" % self.processor[1:])
        f.write("\tinclude\t<%s.inc>\n" % self.processor)
        f.write("\n")

        #  Output configuration settings
        if self.config != []:
            f.write('\t__CONFIG\t')
            s = ''
            for t in self.config:
                s += '_'+t+' & '
            s = s[0:-3]
            f.write(s+'\n\n')

        #  Output code
        for t in self.code:
            if (t[0] != '') and (t[1] == ''):
                f.write("\n%s\n" % t[0])
            elif (t[0] != '') and (t[1] == 'asm'):
                f.write("%s\n" % t[0])
            elif (t[0] != '') and (t[1] != 'equ'):
                f.write("\n%s\n" % t[0])
                f.write("\t%s\t%s\n" % (t[1],t[2]))
            else:
                f.write("%s\t%s\t%s\n" % (t[0],t[1],t[2]))

        f.write("\n\tEND\n")
        f.close()

    
    ########################################################
    #  CompileFile
    #
    def CompileFile(self):
        """Compile the file."""

        self.ParseSourceCode()              #  Parse the source text
        self.DetermineProcessor()           #  Set the target processor
        self.ReadPragmas()                  #  Read any pragmas
        self.ReadConfig()                   #  Read any configuration settings
        self.SetupLibraryRoutines()         #  Set which library routines to output and how
        self.IdentifyEquates()              #  User-defined equates
        self.LocateFunctions()              #  Locate functions
        self.GenerateCode()                 #  Output first-pass code
        self.CodeOptimization()             #  Optimize the first-pass code
        self.OutputAsmFile()                #  Output the .asm file
        

############################################################
#  ProcessCommandLine
#
def ProcessCommandLine():
    """Process the command line to get the source, dest and flags"""

    #
    #  Arguments:
    #    pic0 [-flags] src [dest]
    #
    src = dest = flags = ''
    
    if (len(sys.argv) == 1):
        print "\nUse:\n"
        print "%s src.pic0 [out.asm]\n" % sys.argv[0]
        print "Where:\n"
        print "  src.pic0  =  input file name"
        print "  out.asm   =  output file name\n"
        sys.exit(1)

    for s in sys.argv[1:]:
        if (s[0] == '-'):
            flags = s[1:]
        elif (src == ''):
            src = s
        else:
            dest = s

    if (src == ''):
        print "\nA source file must be given.\n"
        sys.exit(1)
    if (src.count('.pic0') == 0):
        print "\nA source file must end with .pic0\n"
        sys.exit(1)
        
    if (dest == ''):
        dest = src[0:-5] + '.asm'
    
    return [src, dest, flags]


############################################################
#  main
#
def main():
    """Compile the input files."""

    #  Process command line arguments
    src, dest, flags = ProcessCommandLine()
    
    #  Create the compiler for this file and process
    c = PIC0Compiler(src=src, dest=dest, flags=flags)
    c.CompileFile()



#  Run if not imported
if __name__ == '__main__':
    main()

#
#  end pic0.py
#
