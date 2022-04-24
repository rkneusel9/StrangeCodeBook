/*
*  file:  family.pl
*
*  Obligatory family relationships example.
*
*  RTK, 14-Apr-2021
*  Last update:  14-Apr-2021
*/

/* Facts */
male(uranus).
male(cronus).
male(zeus).
male(hades).
male(poseidon).
male(ares).
male(hephaestus).
male(hermes).
male(apollo).
male(dionysus).

female(gaia).
female(rhea).
female(hera).
female(demeter).
female(eris).
female(metis).
female(maia).
female(leto).
female(semele).
female(aphrodite).

parent(uranus, cronus).
parent(gaia, cronus).
parent(cronus, zeus).
parent(rhea, zeus).
parent(cronus, hera).
parent(rhea, hera).
parent(cronus, demeter).
parent(rhea, demeter).
parent(cronus, poseidon).
parent(rhea, poseidon).
parent(zeus, ares).
parent(hera, ares).
parent(zeus, hephaestus).
parent(hera, hephaestus).
parent(zeus, eris).
parent(hera, eris).
parent(zeus, athena).
parent(metis, athena).
parent(zeus, hermes).
parent(maia, hermes).
parent(zeus, apollo).
parent(leto, apollo).
parent(zeus, artemis).
parent(leto, artemis).
parent(zeus, dionysus).
parent(semele, dionysus).
parent(uranus, aphrodite).

married(zeus, hera).
married(hephaestus, aphrodite).

/* Rules */
father(X,Y) :- parent(X,Y), male(X).
mother(X,Y) :- parent(X,Y), female(X).
child(X,Y) :- parent(Y,X).
sibling(X,Y) :- parent(P,X), parent(P,Y), dif(X,Y).
brother(X,Y) :- sibling(X,Y), male(X).
sister(X,Y) :- sibling(X,Y), female(X).
grandparent(X,Y) :- parent(X,A), parent(A,Y).
grandfather(X,Y) :- grandparent(X,Y), male(X).
grandmother(X,Y) :- grandparent(X,Y), female(X).
greatgrandparent(X,Y) :- parent(X,A), parent(A,B), parent(B,Y).
greatgrandfather(X,Y) :- greatgrandparent(X,Y), male(X).
greatgrandmother(X,Y) :- greatgrandparent(X,Y), female(X).
cousin(X,Y) :- sibling(A,B), parent(A,X), parent(B,Y), dif(X,Y).
aunt(X,Y) :- sister(X,A), parent(A,Y).
uncle(X,Y) :- brother(X,A), parent(A,Y).
wife(X,Y) :- female(X), (married(X,Y); married(Y,X)).
husband(X,Y) :- male(X), (married(X,Y); married(Y,X)).
paramour(X,Y) :- child(A,X), child(A,Y), \+ married(X,Y), dif(X,Y).

