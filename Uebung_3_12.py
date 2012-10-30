def prefix_set(w):
	w = list(w)		
	
	tmpString = "'', "
	wordCounter = 1
	
	for i in range(0, len(w)):
		for y in range(0, wordCounter):
			tmpString += w[y]
		tmpString += ", "
		wordCounter += 1
		
	return tmpString

print prefix_set("01101")