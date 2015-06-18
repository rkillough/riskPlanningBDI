from __future__ import division
from random import randint

class Node():
	def __init__(self,name,eu,sampleprob,samplessofar):
		self.name = name
		self.eu = eu
		self.sampleprob = sampleprob
		self.samplessofar = samplessofar

siblingcount = 3
totalsample = 100000
n0 = Node("n0", -50, 0.02, 0)
n1 = Node("n1", 5, 0.28, 0)
n2 = Node("n2", 20, 0.7, 0)

nodes = [n0,n1,n2]


def getrandomsample():
	precision = 10000
	r = randint(0,precision-1)   #Note, this will ignore precision in probabilties with more than 3 dp
	distribution = []   #2d array of integer upper and lower bounds corresponding to the action's probabilties
	l = 0 #lower bound
	t = 0 #cumulative prob
	for p in nodes:
		distribution.append([l, ((t+p.sampleprob)*precision)+1])
		l = p.sampleprob*precision
		t = t+p.sampleprob
	for i in range(len(nodes)):
		if(r >= distribution[i][0] and r < distribution[i][1]):
			nodes[i].samplessofar += 1
			return nodes[i]


actualUtility = 0
for n in nodes:
	actualUtility += n.eu / siblingcount



biasedUtility = 0
unbiasedUtility = 0

for i in range(totalsample):
	nodesampled = getrandomsample()
	biasedUtility += nodesampled.eu
	unbiasedUtility += (nodesampled.eu / nodesampled.samplessofar) * (i / siblingcount)

	#print "Sampling "+nodesampled.name+": "+str(nodesampled.samplessofar)+ ", "+ str(biasedUtility) + ", "+str(unbiasedUtility)


print "Actual:" +str(actualUtility)
print biasedUtility/totalsample
print unbiasedUtility/totalsample




