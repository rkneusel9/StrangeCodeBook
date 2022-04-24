(* Generate the sequence of nonsquare integers *)

program nonsquares;

var
   n : integer;

begin
    for n := 1 to 120 do begin
        write(n + trunc(0.5 + sqrt(n)):4);
        if (n mod 10) = 0 then writeln;
    end;
    writeln
end.

