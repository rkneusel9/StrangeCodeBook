;
;  file:  FRACTRAN.scm
;
;  FRACTRAN in Scheme (Racket)
;
;  RTK, 15-Mar-2021
;  Last update:  16-Mar-2021
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;  Parse the command line and load the list of fractions and first integer
(define argv (current-command-line-arguments))
(define prog (file->list (vector-ref argv 0)))
(define num (string->number (vector-ref argv 1)))
(define trace (string->number (vector-ref argv 2)))

;  Run the program
(define (FRACTRAN)
    (do ((i 0 (+ i 1))) (#f)
        (when (= i (length prog)) 
            (when (= trace 0) (display num)(newline))
            (exit))
        (let ((n (* num (list-ref prog i))))
            (when (exact-integer? n) 
                (set! num n)
                (set! i -1)
                (when (= trace 1) (display num)(newline))) ) ))
(FRACTRAN)

