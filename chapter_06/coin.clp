(deftemplate coin "Roman coin facts"
  (slot emperor)
  (slot denomination)
  (slot obverse)
  (slot reverse))

(deffacts coin-facts "ancient Roman coins"
  (coin (emperor Otho)
        (denomination Denarius)
        (obverse "Emperor hd right")
        (reverse "Securitas std left"))
  (coin (emperor Constantine)
        (denomination AE3)
        (obverse "IMP CONSTANTINVS MAX AVG")
        (reverse "VICTORIAE LAETAE PRINC PERP")) )

