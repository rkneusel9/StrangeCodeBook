(* Gotta do it... *)
fun hello () = print "Hello, world!\n";

(* Standard recursive definition *)
fun greetA(n) =
    if (n = 1) then hello()
    else (hello(); greetA(n-1));

(* Pattern definition *)
fun greetB 1 = hello()
  | greetB n = (hello(); greetB(n-1));

