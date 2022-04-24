;
;  file:  family2.clp
;
;  Brothers and sisters with global accumulators.
;
;  RTK, 11-May-2021
;  Last update:  11-May-2021
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defglobal ?*brothers* = (create$))
(defglobal ?*sisters* = (create$))

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
    (parent uranus aphrodite))

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
    (bind ?msg (implode$ (create$ ?x is sister to ?y)))
    (bind ?*sisters* (create$ ?*sisters* ?msg)))

(defrule brother
    (siblings ?x ?y)
    (male ?x)
    (test (neq ?x ?y))
  =>
    (bind ?msg (implode$ (create$ ?x is brother to ?y)))
    (bind ?*brothers* (create$ ?*brothers* ?msg)))

(deffunction brothers ()
    (foreach ?bro ?*brothers*
        (printout t ?bro crlf)))

(deffunction sisters ()
    (foreach ?sis ?*sisters*
        (printout t ?sis crlf)))

