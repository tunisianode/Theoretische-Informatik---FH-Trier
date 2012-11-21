def f3(n):
    return n**4 + 1024
    
def f4(n):
    p = 0.1*n
    return 2**p
    
for i in range(0,1000):
    #i = 2*i
    if (round(f3(i),0) > round(f4(i),0)):
        print(i)

print("335", f3(335), f4(335))        
print("336", f3(336), f4(336))    

# n = 335
# Fuer 2*n => n = 334