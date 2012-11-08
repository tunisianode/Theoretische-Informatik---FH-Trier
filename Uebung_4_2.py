# Aufgabe nicht getestet und divZ aus der Vorlesung nicht implementiert.

def prodZ(x,y): # Funktionsdeklaration - x-fache Addition von y
    i = 0 # Initialisierungen
    z = 0
    if (x < 0):
        x = (0 - x) # neg. Vorz. von x entfernen
        y = (0 - y) # und auf y uebertragen
    for i in range(0,x): # x Durchlaeufe
        z = (z + y) # y wird x-mal zu z addiert
    return z

def modZ(x,y):
    return (x-prodZ(y,divZ(x,y))
    
def teil(x):
    i = 1
    a = 0
    while (i <= x):
        if (modZ(x,i) == 0):
            a = (a + 1)
        i = (i + 1)
    return a

def prim(n):
    a = 0
    i = 3
    primzahl = 2
    while (a < n):
        if (teil(i) == 2):
            a = (a + 1)
            primzahl = i
        i = (i + 1)
    return primzahl