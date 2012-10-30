def concat(L1, L2):
	L1 = L1.split()
	L2 = L2.split()
	
	resultString = ""
	
	for i in range(0, len(L1)):
		for y in range(0, len(L2)):
			resultString += L1[i] + L2[y] + ", "
	
	return resultString
	
print concat("_ ab abb", "b ba")