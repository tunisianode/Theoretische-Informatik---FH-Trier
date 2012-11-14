# test fuer in Frage kommende n ob x=2^n
def cM(x):
    result = 0
    
    for n in range(0, 2**x):
        if (2**n == x):
            result = 1
    
    return result
    
print(cM(0))
print(cM(4))