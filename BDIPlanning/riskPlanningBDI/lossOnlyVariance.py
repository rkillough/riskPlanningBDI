import math
import sys

data = [0]	#this is important for loss only, addition zero value must be included for reference
S = 0	#running variance
M = 0	#running mean

Variance = 0

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
		
#calculates the running variance (and mean) given a reward and probability)
#does so in a "Loss only" way where only negative reward value outcomes are considered
def computeLOVariance(r,p):	
	global M
	global S
	global Variance

	#print(r)
	
	if(r < 0): 
		x = r * p
		data.append(x)
		#print(r*p)
		k = len(data)

		if k == 0:	#if first sample, initialise the mean to its value
			M = x 
		else:
			Mnew = M + (x-M)/k	#compute the new mean
			S = S + (x-M)*(x-Mnew)	#compute the variance
			M = Mnew
	
		if(k>1):
			Variance = S/(k-1)
			#standarddeviation = math.sqrt(S/(k-1))
		else:
			Variance  = 0

while True:
	
	#print("Current mean = "+str(M))
	#print("Current variance = "+str(Variance))

	print("Enter reward to be added: ")
	r = input()
	print("Enter probability of that reward")
	p = input()

	dstring = ""
	for d in data:
		dstring = dstring + str(d) + " "
	#print("Adding "+r+"*"+p+" to "+ dstring)

	computeLOVariance(float(r),float(p))
	
	print("----------------------------------")	
	print("New mean = "+str(M))
	print("New variance = "+str(Variance))
	print("----------------------------------")	



