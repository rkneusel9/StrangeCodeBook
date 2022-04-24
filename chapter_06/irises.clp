;
;  file:  irises.clp
;
;  Implement the iris classifier.
;
;  RTK, 09-May-2021
;  Last update:  15-May-2021
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(deffacts initial-facts ""
  (question "Is petal width <= 0.80?")
  (state 1)
  (startup))

(defrule start "start the program"
  ?r <- (startup)
  =>
  (printout t crlf)
  (printout t "Iris classifier.  Please respond 'y' or 'n' to each question." crlf)
  (printout t crlf)
  (retract ?r))

(defrule ask-question "ask the user a question"
  ?p <- (question ?q)
  =>
  (retract ?p)
  (printout t ?q " ")
  (bind ?resp (readline))
  (assert (response ?resp)))

(defrule output-result "we have a label"
  (label ?label)
  =>
  (printout t crlf "The sample is an instance of ")
  (printout t ?label crlf crlf)
  (halt))

; question 1
(defrule q1-yes ""
  ?q <- (state 1)
  ?r <- (response "y")
  =>
  (retract ?q ?r)
  (assert (label "setosa (0)")))

(defrule q1-no ""
  ?q <- (state 1)
  ?r <- (response "n")
  =>
  (retract ?q ?r)
  (assert (state 2))
  (assert (question "Is petal length <= 4.75?")))

; question 2
(defrule q2-yes ""
  ?q <- (state 2)
  ?r <- (response "y")
  =>
  (retract ?q ?r)
  (assert (state 3))
  (assert (question "Is petal width <= 1.65?")))

(defrule q2-no ""
  ?q <- (state 2)
  ?r <- (response "n")
  =>
  (retract ?q ?r)
  (assert (state 4))
  (assert (question "Is petal width <= 1.75?")))

; question 3
(defrule q3-yes ""
  ?q <- (state 3)
  ?r <- (response "y")
  =>
  (retract ?q ?r)
  (assert (label "versicolor (1)")))

(defrule q3-no ""
  ?q <- (state 3)
  ?r <- (response "n")
  =>
  (retract ?q ?r)
  (assert (label "virginica (2)")))

; question 4
(defrule q4-yes ""
  ?q <- (state 4)
  ?r <- (response "y")
  =>
  (retract ?q ?r)
  (assert (state 5))
  (assert (question "Is petal length <= 5.05?")))

(defrule q4-no ""
  ?q <- (state 4)
  ?r <- (response "n")
  =>
  (retract ?q ?r)
  (assert (state 6))
  (assert (question "Is petal length <= 4.85?")))

; question 5
(defrule q5-yes ""
  ?q <- (state 5)
  ?r <- (response "y")
  =>
  (retract ?q ?r)
  (assert (label "versicolor (1)")))

(defrule q5-no ""
  ?q <- (state 5)
  ?r <- (response "n")
  =>
  (retract ?q ?r)
  (assert (state 7))
  (assert (question "Is sepal length <= 6.05?")))

; question 6
(defrule q6-yes ""
  ?q <- (state 6)
  ?r <- (response "y")
  =>
  (retract ?q ?r)
  (assert (state 8))
  (assert (question "Is sepal length <= 5.95?")))

(defrule q6-no ""
  ?q <- (state 6)
  ?r <- (response "n")
  =>
  (retract ?q ?r)
  (assert (label "virginica (2)")))

; question 7
(defrule q7-yes ""
  ?q <- (state 7)
  ?r <- (response "y")
  =>
  (retract ?q ?r)
  (assert (label "versicolor (1)")))

(defrule q7-no ""
  ?q <- (state 7)
  ?r <- (response "n")
  =>
  (retract ?q ?r)
  (assert (label "virginica (2)")))

; question 8
(defrule q8-yes ""
  ?q <- (state 8)
  ?r <- (response "y")
  =>
  (retract ?q ?r)
  (assert (label "versicolor (1)")))

(defrule q8-no ""
  ?q <- (state 8)
  ?r <- (response "n")
  =>
  (retract ?q ?r)
  (assert (label "virginica (2)")))

; end irises.clp

