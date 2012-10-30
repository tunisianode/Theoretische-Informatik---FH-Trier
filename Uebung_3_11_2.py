def reverse_set_of_words(L):
	L = L.split()

	tmpString = ""
	for i in range(len(L), 0, -1):
		tmpString += L[i-1] + " "

	return tmpString

print reverse_set_of_words("erste zweite dritte")