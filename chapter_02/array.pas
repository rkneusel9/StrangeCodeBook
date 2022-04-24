program xyzzy;

var
    A : array[0..99,0..511,0..511] of real;
    i,j,k : integer;

begin
  (* code to fill in A *)
  randomize;
  for i:= 0 to 99 do
    for j:= 0 to 511 do
      for k:= 0 to 511 do
        A[i,j,k] := random(256);

  (* scale A [0,1] *)
  for i:= 0 to 99 do
    for j:= 0 to 511 do
      for k:= 0 to 511 do
        A[i,j,k] := A[i,j,k] / 256.0;
end.

