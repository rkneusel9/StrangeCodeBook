/*  Facts about animals  */
alive(mollie).
alive(strider).
alive(lily).
alive(patches).
dead(sombra).
dead(ruby).
dead(gabby).
dead(perdita).
bordercollie(mollie).
bordercollie(patches).
malinois(strider).
dog(mollie).
dog(strider).
dog(patches).
cat(lily).
fish(perdita).

breed(mollie, bordercollie).
breed(patches, bordercollie).
breed(strider, malinois).

/* Rules */
warm(X) :- dog(X); cat(X).
cold(X) :- fish(X); dead(X).
mammal(X) :- (dog(X); cat(X)), alive(X).

