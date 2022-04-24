#
#  file:  ball_search_7.py
#
#  Evolve 1000 successful ball0.txt 7-instruction programs.
#
#  RTK, 29-Jan-2021
#  Last update:  29-Jan-2021
#
################################################################

import time
import sys
import os
import numpy as np

#
#  Genetic algorithm code, see "Swarm Optimization" (Kneusel, MIT Press, 2021)
#  MIT License
#

################################################################
#  RandomInitializer
#
class RandomInitializer:
    """Initialize a swarm uniformly"""

    #-----------------------------------------------------------
    #  __init__
    #
    def __init__(self, npart=10, ndim=3, bounds=None):
        """Constructor"""

        self.npart = npart
        self.ndim = ndim
        self.bounds = bounds


    #-----------------------------------------------------------
    #  InitializeSwarm
    #
    def InitializeSwarm(self):
        """Return a randomly initialized swarm"""

        if (self.bounds == None):
            #  No bounds given, just use [0,1)
            self.swarm = np.random.random((self.npart, self.ndim))
        else:
            #  Bounds given, use them
            self.swarm = np.zeros((self.npart, self.ndim))
            lo = self.bounds.Lower()
            hi = self.bounds.Upper()

            for i in range(self.npart):
                for j in range(self.ndim):
                    self.swarm[i,j] = lo[j] + (hi[j]-lo[j])*np.random.random()        
            self.swarm = self.bounds.Limits(self.swarm)

        return self.swarm


################################################################
#  Bounds
#
class Bounds:
    """Base bounds class"""

    #-----------------------------------------------------------
    #  __init__
    #
    #  Supply lower and upper bounds for each dimension.
    #
    def __init__(self, lower, upper, enforce="clip"):
        """Constructor"""

        self.lower = np.array(lower)
        self.upper = np.array(upper)
        self.enforce = enforce.lower() # clip | resample


    #-----------------------------------------------------------
    #  Upper
    #
    #  Return a vector of the per dimension upper limits.
    #
    def Upper(self):
        """Upper bounds"""

        return self.upper


    #-----------------------------------------------------------
    #  Lower
    #
    def Lower(self):
        """Lower bounds"""

        return self.lower


    #-----------------------------------------------------------
    #  Limits
    #
    def Limits(self, pos):
        """Apply the selected boundary conditions"""

        npart, ndim = pos.shape

        for i in range(npart):
            if (self.enforce == "resample"):
                for j in range(ndim):
                    if (pos[i,j] <= self.lower[j]) or (pos[i,j] >= self.upper[j]):
                        pos[i,j] = self.lower[j] + (self.upper[j]-self.lower[j])*np.random.random()
            else:  # clip
                for j in range(ndim):
                    if (pos[i,j] <= self.lower[j]):
                        pos[i,j] = self.lower[j]
                    if (pos[i,j] >= self.upper[j]):
                        pos[i,j] = self.upper[j]
            
            #  Also validate
            pos[i] = self.Validate(pos[i])

        return pos


    #-----------------------------------------------------------
    #  Validate
    #
    #  For example, override this to enforce a discrete position
    #  for a particular vector.
    #
    def Validate(self, pos):
        """Validate a given position vector"""

        return pos


################################################################
#  GA
#
class GA:
    """Genetic algorithm"""

    #-----------------------------------------------------------
    #  __init__
    #
    def __init__(self, obj,       # the objective function (subclass Objective)
                 npart=10,        # number of particles in the swarm
                 ndim=3,          # number of dimensions in the swarm
                 max_iter=200,    # maximum number of steps
                 CR=0.8,          # cross-over probability
                 F=0.05,          # mutation probability
                 top=0.5,         # top fraction (only breed with the top fraction)
                 tol=None,        # tolerance (done if no done object and gbest < tol)
                 init=None,       # swarm initialization object (subclass Initializer)
                 done=None,       # custom Done object (subclass Done)
                 bounds=None):    # swarm bounds object

        self.obj = obj
        self.npart = npart
        self.ndim = ndim
        self.max_iter = max_iter
        self.init = init
        self.done = done
        self.bounds = bounds
        self.tol = tol
        self.CR = CR
        self.F = F
        self.top = top
        self.initialized = False


    #-----------------------------------------------------------
    #  Results
    #
    def Results(self):
        """Return the current results"""

        if (not self.initialized):
            return None

        return {
            "npart": self.npart,            # number of particles
            "ndim": self.ndim,              # number of dimensions 
            "max_iter": self.max_iter,      # maximum possible iterations
            "iterations": self.iterations,  # iterations actually performed
            "tol": self.tol,                # tolerance value, if any
            "gbest": self.gbest,            # sequence of global best function values
            "giter": self.giter,            # iterations when global best updates happened
            "gpos": self.gpos,              # global best positions
            "gidx": self.gidx,              # particle number for new global best
            "pos": self.pos,                # current particle positions
            "vpos": self.vpos,              # and objective function values
        }


    #-----------------------------------------------------------
    #  Initialize
    #
    def Initialize(self):
        """Set up the swarm"""

        self.initialized = True
        self.iterations = 0
       
        self.pos = self.init.InitializeSwarm()  # initial swarm positions
        self.vpos= self.Evaluate(self.pos)      # and objective function values

        #  Swarm bests
        self.gidx = []
        self.gbest = []
        self.gpos = []
        self.giter = []

        self.gidx.append(np.argmin(self.vpos))
        self.gbest.append(self.vpos[self.gidx[-1]])
        self.gpos.append(self.pos[self.gidx[-1]].copy())
        self.giter.append(0)


    #-----------------------------------------------------------
    #  Done
    #
    def Done(self):
        """Check if we are done"""

        if (self.done == None):
            if (self.tol == None):
                return (self.iterations == self.max_iter)
            else:
                return (self.gbest[-1] < self.tol) or (self.iterations == self.max_iter)
        else:
            return self.done.Done(self.gbest,
                        gpos=self.gpos,
                        pos=self.pos,
                        max_iter=self.max_iter,
                        iteration=self.iterations)


    #-----------------------------------------------------------
    #  Evaluate
    #
    def Evaluate(self, pos):
        """Evaluate a set of positions"""

        p = np.zeros(self.npart)
        for i in range(self.npart):
            p[i] = self.obj.Evaluate(pos[i])
        return p


    #-----------------------------------------------------------
    #  Mutate
    #
    def Mutate(self, idx):
        """Return a mutated position vector"""

        j = np.random.randint(0,self.ndim)
        if (self.bounds != None):
            self.pos[idx,j] = self.bounds.lower[j] + np.random.random()*(self.bounds.upper[j]-self.bounds.lower[j])
        else:
            lower = self.pos[:,j].min()
            upper = self.pos[:,j].max()
            self.pos[idx,j] = lower + np.random.random()*(upper-lower)


    #-----------------------------------------------------------
    #  Crossover
    #
    def Crossover(self, a, idx):
        """Mate with another swarm member"""

        #  Get the partner in the top set
        n = int(self.top*self.npart)
        b = idx[np.random.randint(0, n)]
        while (a==b):
            b = idx[np.random.randint(0, n)]

        #  Random cut-off position
        d = np.random.randint(0, self.ndim)

        #  Crossover
        t = self.pos[a].copy()
        t[d:] = self.pos[b,d:]
        self.pos[a] = t.copy()


    #-----------------------------------------------------------
    #  Evolve
    #
    def Evolve(self):
        """Evolve the swarm"""

        idx = np.argsort(self.vpos)

        for k,i in enumerate(idx):
            if (k == 0):
                continue    #  leave the best one alone
            if (np.random.random() < self.CR):
                #  Breed this one with one of the better particles
                self.Crossover(i, idx)
            if (np.random.random() < self.F):
                #  Random mutation
                self.Mutate(i)

        if (self.bounds != None):
            self.pos = self.bounds.Limits(self.pos)


    #-----------------------------------------------------------
    #  Step
    #
    def Step(self):
        """Do one swarm step"""

        self.Evolve()                               # evolve the swarm
        self.vpos = self.Evaluate(self.pos)         # and evaluate the new positions

        #  For each particle
        for i in range(self.npart):
            if (self.vpos[i] < self.gbest[-1]):         # is new position global best?
                self.gbest.append(self.vpos[i])         # new position is new swarm best
                self.gpos.append(self.pos[i].copy())    # keep the position
                self.gidx.append(i)                     # particle number
                self.giter.append(self.iterations)      # and when it happened

        self.iterations += 1


    #-----------------------------------------------------------
    #  Optimize
    #
    def Optimize(self):
        """Run a full optimization and return the best"""

        self.Initialize()

        while (not self.Done()):
            self.Step()

        return self.gbest[-1], self.gpos[-1]


#
#  For "Strange Code" (Kneusel, No Starch Press, 2021)
#  MIT License
#

#  Allowed program characters
DIGITS= ["0","1","2","3","4","5","6","7","8","9"]
MOVES = ["N","E","W","S"]
OTHER = ["M","I","D"]
ALLOWED = DIGITS + MOVES + OTHER


################################################################
#  Firefly
#
class Firefly:
    """A reduced-instruction Firefly interpreter"""

    #-----------------------------------------------------------
    #  Move
    #
    def Move(self, c):
        """Move according to the current mode"""

        #  Apply current mode
        if self.M == "M":
            pass
        elif self.M == "I":
            self.C[self.I] += 1
            if self.C[self.I] > 9:
                self.C[self.I] =0
        elif self.M == "D":
            if (self.C[self.I] == 0):
                self.C[self.I] = 9
            else:
                self.C[self.I] -= 1
        else:
            self.C[self.I] = int(self.M)

        #  Now move somewhere
        i = self.I // 5
        j = self.I % 5

        if c == "N":
            i -= 1
            if i < 0:
                i = 4
        elif c == "S":
            i += 1
            if i > 4:
                i = 0
        elif c == "E":
            j += 1
            if j > 4:
                j = 0
        elif c == "W":
            j -= 1
            if j < 0:
                j = 4
        
        self.I = 5*i + j


    #-----------------------------------------------------------
    #  Run
    #
    def Run(self):
        """Run a move-only Firefly program"""
       
        for c in self.prg:
            if c == "I":
                self.M = "I"
            elif c == "D":
                self.M = "D"
            elif c == "M":
                self.M = "M"
            elif c in self.DIGITS:
                self.M = c
            elif c in self.MOVES:
                self.Move(c)


    #-----------------------------------------------------------
    #  GetDisplay
    #
    def GetDisplay(self):
        """Return the display as a 5x5 array"""

        return self.C.reshape((5,5))


    #-----------------------------------------------------------
    #  __init__
    #
    def __init__(self, prg=None):
        """Constructor"""
        
        self.prg = prg
        self.C = np.zeros(25)
        self.I = 12
        self.M = "M"
        self.DIGITS= ["0","1","2","3","4","5","6","7","8","9"]
        self.MOVES = ["N","E","W","S"]


################################################################
#  FlyBounds
#
class FlyBounds(Bounds):
    """Bounds for Firefly programs"""

    def __init__(self, ndim):
        lower = [0]*ndim
        upper = [len(ALLOWED)-1]*ndim
        super().__init__(lower, upper, enforce="resample")

    def Validate(self, p):
        return np.floor(p+0.5)


################################################################
#  PositionToFirefly
#
def PositionToFirefly(p):
    """Map a position to Firefly program text"""

    prg = ""
    for i in range(len(p)):
        prg += ALLOWED[int(p[i])]
    return prg 


################################################################
#  FlyObjective
#
class FlyObjective:
    """Objective function"""

    def __init__(self, target):
        """Constructor"""
        self.target = target
        self.fcount = 0

    def Evaluate(self, p):
        """Evaluate a program"""
        self.fcount += 1
        prg = PositionToFirefly(p)
        fly = Firefly(prg)
        fly.Run()
        return ((self.target - fly.GetDisplay())**2).mean()


################################################################
#  main
#
def main():
    """Evolve 1000 7-instruction ball0.txt programs"""

    target = np.loadtxt("ball/ball0.txt")
    npart = 30
    ndim = 7
    niter = 10000

    progs = []

    k = 0
    while (k < 1000):
        b = FlyBounds(ndim)
        i = RandomInitializer(npart, ndim, bounds=b)
        obj = FlyObjective(target)
        swarm = GA(obj=obj, npart=npart, ndim=ndim, init=i, tol=1e-12, max_iter=niter, bounds=b)
        swarm.Optimize()
        res = swarm.Results()

        if (res["gbest"][-1] == 0.0):
            prg = PositionToFirefly(res["gpos"][-1])
            progs.append(prg)
            k += 1
            print("%4d: %s" % (k, prg))

    print()

    with open("ball_search_7_results.txt","w") as f:
        for p in progs:
            f.write("%s\n" % p)


if (__name__ == "__main__"):
    main()

