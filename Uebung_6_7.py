def f1(n):
    return 23*n**2+3
    
def f2(n):
    return 0.5*n**3-7
    
for i in range(0, 100000):
    if (f1(i) > f2(i)):
        print(i)
        
for i in range(0, 100000):
    if (f1(2*i) > f2(2*i)):
        print(i)
        
print(f1(46), f2(46)) # Hier springt die Seite um
print(f1(47), f2(47))

# Aufgabe 1
# n = 46

# Fuer 2*n ist n = 23