def g(x):
	if (x == 0):
		return 0
	else:
		return g(x-1) + x**3 # x**3 aequivalent zu x^3
		
def sollwert():
	if (g(1) == 1):
		return 1
	else:
		return 0

print sollwert()