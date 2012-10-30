def reverse_word(w):
	x = list(w)		
	resultString = ""
	
	for i in range(len(x), 0, -1):
		resultString += x[i-1]
	
	return resultString
	
print reverse_word("Hochschule")