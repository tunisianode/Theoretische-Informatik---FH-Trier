# Primzahlen: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
# n >= 2 && p,q mit 2n = p + q

from Tools import prim
    
def cM(n):
    sum = 2**n
    result = 0
    a = prim(n)
    while (n > 0):
        m = n
        while (m > 0):
            if (prim(m)+prim(n) == sum):
                result = 1
            m = (m - 1)
        n = (n-1)
        
    return result

print(cM(3))