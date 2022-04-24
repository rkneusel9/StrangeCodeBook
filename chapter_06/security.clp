(defrule react-security-breach "React to a security breach"
    ?r <- (security-breach ?typ)
  =>  
    (retract ?r) 
    (assert (log-security-breach ?typ))
    (printout t "!!! security alert !!!" crlf))

