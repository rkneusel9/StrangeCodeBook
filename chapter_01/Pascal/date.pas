(* For Data General Pascal circa 1986 *)

program date(input,output);

var
   k,d,c,w : integer;
   m : real;

begin
   writeln('This program will tell you what day of the week any date');
   writeln('was, enter the month starting with March as 1 and treat');
   writeln('Jan and Feb as months 11 & 12 of the year before.');
   writeln;
   writeln('Jan  Feb  Mar  Apl  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec');
   writeln(' 11   12   1    2    3    4    5    6    7    8    9   10');
   writeln;
   write('Enter the month: ');
   readln(m);
   write('Enter the day: ');
   readln(k);
   write('Enter the century: ');
   readln(c);
   write('Enter the year: ');
   readln(d);
   w:=(trunc(2.6*m-0.2)+k+d+trunc(d/4.0)+trunc(c/4.0)-2*c) mod 7;
   if w<0 then w:=w+7;
   writeln;
   writeln;
   write('That day is a ');
   case w of
    0 : writeln('Sunday');
    1 : writeln('Monday');
    2 : writeln('Tuesday');
    3 : writeln('Wednesday');
    4 : writeln('Thursday');
    5 : writeln('Friday');
    6 : writeln('Saturday');
   end;
   writeln
end.

