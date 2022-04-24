;
;  file:  math.clp
;
;  A simple calculator in CLIPS.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule start ""
  ?r <- (startup)
  =>
  (printout t "A simple calculator." crlf)
  (printout t crlf)
  (printout t "Enter <number> <op> <number> where" crlf)
  (printout t "<op> is +, -, *, /, ^, mod" crlf crlf)
  (printout t "Enter <function> <arg> where" crlf)
  (printout t "      <function> is: trig, log, exp, or sqrt" crlf crlf)
  (printout t "Type 'end' to exit and @ to use the previous result." crlf)
  (retract ?r)
  (assert (get-next-operation)))

(defrule unary-math ""
  ?w <- (operation ?func ?x)
  ?at <- (@ ?last)
  =>
  (retract ?w)
  (retract ?at)
  (assert (get-next-operation))
  (if (eq ?x @) then (bind ?x ?last))
  (if (eq ?func cos) then (bind ?y (cos ?x)))
  (if (eq ?func sin) then (bind ?y (sin ?x)))
  (if (eq ?func tan) then (bind ?y (tan ?x)))
  (if (eq ?func log) then (bind ?y (log ?x)))
  (if (eq ?func exp) then (bind ?y (exp ?x)))
  (if (eq ?func sqrt) then (bind ?y (sqrt ?x)))
  (printout t ?y)
  (assert (@ ?y)))
  
(defrule binary-math ""
  ?w <- (operation ?a ?op ?b)
  ?at <- (@ ?last)
  =>
  (retract ?w)
  (retract ?at)
  (assert (get-next-operation))
  (if (eq ?a @) then (bind ?a ?last))
  (if (eq ?b @) then (bind ?b ?last))
  (if (eq ?op +) then (bind ?y (+ ?a ?b)))
  (if (eq ?op -) then (bind ?y (- ?a ?b)))
  (if (eq ?op *) then (bind ?y (* ?a ?b)))
  (if (eq ?op /) then (bind ?y (/ ?a ?b)))
  (if (eq ?op ^) then (bind ?y (** ?a ?b)))
  (if (eq ?op mod) then (bind ?y (mod ?a ?b)))
  (printout t ?y)
  (assert (@ ?y)))
    
(defrule get-operation ""
  ?w <- (get-next-operation)
  =>
  (retract ?w)
  (printout t crlf "      ")
  (bind ?expr (readline))
  (if (eq ?expr "end") then (halt))
  (assert (operation (explode$ ?expr))) )
  
(deffacts initial-facts ""
  (@ 0)
  (startup))

