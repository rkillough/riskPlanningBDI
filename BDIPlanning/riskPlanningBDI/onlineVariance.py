import sys

data = []
S = 0	#running variance
M = 0	#running mean

def computeOnlineVariance(x):	#x will be the new value weve just sampled
	global M
	global S

	data.append(x)
	k = len(data)

	if k == 0:	#if first sample, initialise the mean to its value
		M = x
	else:
		Mnew = M + (x-M)/k	#compute the new mean
		S = S + (x-M)*(x-Mnew)
		M = Mnew


while True:
	global x

	print("Current mean = "+str(M))
	print("Current variance = "+str(S))

	print("Enter value to be added: ")
	x = input()

	dstring = ""
	for d in data:
		dstring = dstring + str(d) + " "
	print("Adding "+str(x)+" to "+ dstring)

	newVar = computeOnlineVariance(int(x))
	
	print("\nNew mean = "+str(M))
	print("New variance = "+str(S))
	



