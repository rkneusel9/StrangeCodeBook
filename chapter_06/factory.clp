;
;  Monitor a factory
;

;  Base time
(defglobal ?*base* = (time))
(deffunction ftime ()
  (- (time) ?*base*))

;  Simple random numbers, [0,1)
(deffunction rand ()
  (/ (mod (random) 1000000) 1000000))

;  Pause execution for a few seconds
(deffunction pause (?delay)
  (bind ?start (time))
  (while (< (time) (+ ?start ?delay)) do))

;
;  Rules to respond to things in the factory
;
(defrule emergency "there is an emergency"
    (declare (salience 100))
    ?x <- (emergency-alert)
  =>
    (retract ?x)
    (printout t "  !!! emergency! !!!" crlf))

(defrule pumps-on "turn the pumps on"
    (declare (salience 5))
    ?x <- (pumps-on)
  =>
    (retract ?x)
    (printout t "  pumps on (" (ftime) ")" crlf)
    (assert (pumps-off-time (+ (ftime) 3))))

(defrule pumps-off "turn off the pumps"
    (declare (salience 5))
    ?x <- (pumps-off-time ?t)
  =>
    (if (>= (ftime) ?t) then 
      (retract ?x)
      (printout t "  pumps off (" (ftime) ")" crlf)
    else
      (refresh pumps-off)))

;
;  Main monitor rule
;
(defrule monitor "monitor the factory"
    (declare (salience 0))
    (monitor-loop)
  =>
    ; Simulate events
    (if (< (rand) 0.2) then (assert (pumps-on)))
    (if (< (rand) 0.05) then (assert (emergency-alert)))

    ; Pause then monitor again
    (pause 0.2)
    (refresh monitor))

;  Set up initial facts
(deffacts initial
  (monitor-loop))

