MODULE loops;

(* Structured programming loop demo, RTK, 27-Apr-2021 *)

FROM StrIO IMPORT WriteString, WriteLn;
FROM NumberIO IMPORT WriteCard;

VAR
    i : CARDINAL;

BEGIN
  WriteString("Top tested:");  WriteLn;
  WriteString("  index:");
  i := 0;
  WHILE (i < 6) DO
    WriteCard(i,3);
    i := i + 1;
  END;
  WriteLn;

  WriteString("Bottom tested:");  WriteLn;
  WriteString("  index:");
  i := 0;
  REPEAT
    WriteCard(i,3);
    i := i + 1;
  UNTIL i = 6;
  WriteLn;

  WriteString("Loop:");  WriteLn;
  WriteString("  index:");
  i := 0;
  LOOP
    WriteCard(i,3);
    i := i + 1;
    IF i = 6 THEN 
      EXIT;
    END;
  END;
  WriteLn;

  WriteString("Counted:");  WriteLn;
  WriteString("  index:");
  FOR i := 0 TO 5 DO
    WriteCard(i,3);
  END;
  WriteLn;
END loops.

