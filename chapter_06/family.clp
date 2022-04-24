;
;  file:  family.clp
;
;  Relationships in CLIPS
;
;  RTK, 11-May-2021
;  Last update:  11-May-2021
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(deffacts olympians
    (male uranus)
    (male cronus)
    (male zeus)
    (male hades)
    (male poseidon)
    (male ares)
    (male hephaestus)
    (male hermes)
    (male apollo)
    (male dionysus)
    (female gaia)
    (female rhea)
    (female hera)
    (female demeter)
    (female eris)
    (female metis)
    (female maia)
    (female leto)
    (female semele)
    (female aphrodite)
    (female artemis)
    (parent uranus cronus)
    (parent gaia cronus)
    (parent cronus zeus)
    (parent rhea zeus)
    (parent cronus hera)
    (parent rhea hera)
    (parent cronus demeter)
    (parent rhea demeter)
    (parent cronus poseidon)
    (parent rhea poseidon)
    (parent zeus ares)
    (parent hera ares)
    (parent zeus hephaestus)
    (parent hera hephaestus)
    (parent zeus eris)
    (parent hera eris)
    (parent zeus athena)
    (parent metis athena)
    (parent zeus hermes)
    (parent maia hermes)
    (parent zeus apollo)
    (parent leto apollo)
    (parent zeus artemis)
    (parent leto artemis)
    (parent zeus dionysus)
    (parent semele dionysus)
    (parent uranus aphrodite)
    (married zeus hera)
    (married hephaestus aphrodite))

(defrule father
    (parent ?x ?y)
    (male ?x)
  =>
    (printout t ?x " is father of " ?y crlf))

(defrule mother
    (parent ?x ?y) 
    (female ?x)
  =>
    (printout t ?x " is mother of " ?y crlf))

(defrule sibling
    (parent ?p ?x)
    (parent ?p ?y)
    (test (neq ?x ?y))
  =>
    (assert (siblings ?x ?y)))

(defrule sister
    (siblings ?x ?y)
    (female ?x)
    (test (neq ?x ?y))
  =>
    (printout t ?x " is sister to " ?y crlf))

(defrule brother
    (siblings ?x ?y)
    (male ?x)
    (test (neq ?x ?y))
  =>
    (printout t ?x " is brother to " ?y crlf))

(defrule grandparent
    (parent ?x ?a)
    (parent ?a ?y)
  =>
    (assert (grandparent-of ?x ?y)))

(defrule grandmother
    (grandparent-of ?x ?y)
    (female ?x)
  =>
    (printout t ?x " is grandmother of " ?y crlf))

(defrule grandfather
    (grandparent-of ?x ?y)
    (male ?x)
  =>
    (printout t ?x " is grandfather of " ?y crlf))

(defrule wife
    (female ?x)
    (or (married ?x ?y) (married ?y ?x))
  =>
    (printout t ?x " is wife of " ?y crlf))

(defrule husband
    (male ?x)
    (or (married ?x ?y) (married ?y ?x))
  =>
    (printout t ?x " is husband of " ?y crlf))

