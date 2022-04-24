program LBB;

type
    PhoneNumberType = record
        area, exchange, number : Integer;
    end;

    BirthdayType = record
        month, day, year : Integer;
    end;

    PersonType = record
        first, last : string;
        address : string;
        phone : PhoneNumberType;
        bday : BirthdayType;
     end;

var
    i : integer;
    firsts : array [1..7] of string = 
                ('Winston','Harold','Red','Mike','Dalton','Ed','Edgar');
    lasts : array [1..7] of string =
                ('Rothschild','Green','Green','Hamar','Humphrey','Frid','Montrose');
    streets : array [1..6] of string =
                ('Mockingbird Ln', 'Evergreen Terrace', 'Hauser Street',
                 'E. 68th Street', 'Candlewood Lane', 'Maple St.');
    book : array [1..100] of PersonType;

begin
    randomize;

    for i := 1 to 100 do begin
        with book[i] do begin
            first := firsts[1+random(6)];
            last := lasts[1+random(6)];
            bday.year := 1900 + random(100);
            bday.day := random(29);
            bday.month := 1 + random(12);
            phone.number := 1000 + random(9000);
            phone.exchange := 100 + random(900);
            phone.area := 100 + random(900);
            address := streets[1+random(5)];
        end;
    end;

    for i := 1 to 100 do begin
        with book[i] do begin
            write('birthday: ', bday.year);
            write('/', bday.month:2, '/', bday.day:2);
            write(', phone: ', phone.area);
            write('-', phone.exchange);
            write('-', phone.number);
            write(', address: ', address:17);
            writeln(', name: ', first, ' ', last);
        end;
    end
end.

