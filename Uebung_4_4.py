def prodZ(x,y): # Funktionsdeklaration - x-fache Addition von y
    i = 0 # Initialisierungen
    z = 0
    if (x < 0):
        x = (0 - x) # neg. Vorz. von x entfernen
        y = (0 - y) # und auf y uebertragen
    for i in range(0,x): # x Durchlaeufe
        z = (z + y) # y wird x-mal zu z addiert
    return z

def faku1(x):
    result = 1
    if (x<1):
        result=1
    else:
        x = (x+1)
        for i in range(1,x):
            result = prodZ(result,i)
    return result
    
def faku2(x):
    result=0
    if (x<1):
        result = 1
    else:
        result = prodZ(faku2(x-1), x)
        
    return result
    
def faku3(x):
    result=1    
    while (x>0):
        result = prodZ(result,x)
        x = (x-1)
        
    return result