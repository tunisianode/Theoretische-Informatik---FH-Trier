from math import sqrt

def fib(x):
	if (x == 0):
		return 0
	elif (x == 1):	
		return 1
	else:
		return fib(x-1) + fib(x-2)
		
def sollwert(n):
	if n >= 1 :
		return round((1/sqrt(5))*((((1+sqrt(5))/2)**n))-(((1-sqrt(5))/2)**n))
		
print fib(10)
print sollwert(10)
