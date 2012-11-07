def g(x):
    return (x+x) # Es darf kein *-Zeichen verwendet werden.

def f(x):   
    result = 1
   
    while(x > 0):
        result = g(result)
        x = (x-1)
    
    return result