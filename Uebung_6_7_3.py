import math   # This will import math module

# math.log funktioniert hier irgendwie nicht.

def f5(n):
    return 51*n*log(n)
    
def f6(n):
    return n**2
    
for i in range(0, 1000):
    if (f5(i) > f6(i)):
        print(i)
        
