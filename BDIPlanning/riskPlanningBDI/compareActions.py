#This program alows the construciton of two actionsa and any number of probabilistic resulting states form those action
#It then calculates the utility and the variance of each action and outputs the results

import math

#an action consists of a name and a list of resulting states
class action:
	def __init__(self,name,states):
		self.name = name
		self.states = states

#A state consists of a name, a reward value and a probability of occurance
class state:		
	def __init__(self,name,reward,prob):
		self.name = name
		self.reward = reward
		self.prob = prob

#S0
s1 = state("shot",-2000,0.05)
sa = state("injured",-1000,0.1)
sb = state("PTSD",-900,0.15)	
s2 = state("kill someone",-100,0.2)
sc = state("help someone",100,0.5)	
s3 = state("burnt",-15,0.95)	
s4 = state("notburnt",0,0.05)
	
a1 = action("army",[s1,s2,sa,sb,sc])
a2 = action("cookery",[s3,s4])


#S1
s5 = state("cross2",1,0.99)	
s6 = state("dontcross2",-1500,0.01)	
s7 = state("cross4",1,0.98)	
s8 = state("dontcross4",-1500,0.02)	

a3 = action("cross2lane",[s5,s6])
a4 = action("cross4lane",[s7,s8])


#THis demonstrates that variance isnt that great of a risk measure
s9 = state("lose",0,0.8)
s10 = state("win",100,0.2)

s11 = state("lose",0,0.9)
s12 = state("win",100,0.1)

a5 = action(".2 chance of $100",[s9,s10])
a6 = action(".1 chance of $100",[s11,s12])

def calculateUtility(action):
	#print("Calculating the utility of "+action.name)
	total = 0
	for s in action.states:
		total = total + s.reward * s.prob
	return total 

def calculateVariance(action):
	#print("Calculating the variance")
	avg = calculateUtility(action) / len(action.states)			#this is innefficient, weve already calculated utility
	
	totalVariance = 0
	for s in action.states:
		variance = math.pow((s.reward*s.prob)-avg, 2)
		totalVariance = totalVariance + variance

	avgVariance = totalVariance / len(action.states)	#not sure we should do this, just seems right
	return avgVariance


#This is the naive algorithm on wikipedia, it is funcitonally equivalent to my calculation above
#However the article says not to use this due 
def otherVariance(action):
	n = 0
	Sum = 0
	Sum_sqr = 0

	for s in action.states:
		x = s.prob * s.reward
		n += 1
		Sum += x
		Sum_sqr += x*x
	variance = (Sum_sqr - (Sum*Sum)/n)/n
	return variance

#This is the non-naive variance algorithm, I am so far unable to find any different results than the naive one
def shifted_data_variance(action):

	data = action.states

	if len(data) == 0:
		return 0
	K = data[0].prob*data[0].reward
	n = 0
	Sum = 0
	Sum_sqr = 0
	for x in data:
		u = x.reward*x.prob
		n = n + 1
		Sum += u - K
		Sum_sqr += (u - K) * (u - K)
	variance = (Sum_sqr - (Sum * Sum)/n)/(n)
	# use n instead of (n-1) if want to compute the exact variance of the given data
	# use (n-1) if data are samples of a larger population
	return variance

#This algorithm computes variance for an action but only considers negative values plus a fake zero value
#If a zero value is already present anyway, then a new one is not added, I don't know if this is corrent behavior yet
def lossOnlyVariance(action):

	applicableStates = []	
	#remove states which contain postive rewards, we are not interested in these
	for s in action.states:
		if (s.reward < 0):
			applicableStates.append(s)

	if(len(applicableStates) > 0):
		total = 0
		for s in applicableStates:
			val = s.prob * s.reward
			print(val)
			total = total + val
	
		avgLoss = total/ (len(applicableStates)+1)	#this +1 is effectively adding an additional zero value
		print ("avg: "+str(avgLoss))
		
		totalVariance = 0
		for s in applicableStates:
			variance = math.pow((s.reward*s.prob)-avgLoss, 2)
			totalVariance = totalVariance + variance
	
		avgVariance = totalVariance / len(applicableStates)
		return avgVariance
	else:
		return 0

def compareActions(action1, action2):

	if(checkValidAction(action1)):
		print("Utility of "+action1.name+": "+str(calculateUtility(action1)))
		print("Variance (risk) of "+action1.name+": "+str(calculateVariance(action1)))
		print("Loss only variance: "+str(lossOnlyVariance(action1)))

	if(checkValidAction(action2)):
		print("Utility of "+action2.name+": "+str(calculateUtility(action2)))
		print("Variance (risk) of "+action2.name+": "+str(calculateVariance(action2)))
		print("Loss only variance: "+str(lossOnlyVariance(action2)))


#Make sure all the probabilities of the outcomes add up to 1
def checkValidAction(action):
	sum = 0
	for s in action.states:
		#print(s.prob)
		sum = sum + s.prob
	if(round(sum,10) == 1):
		return True
	else:
		print(sum)
		print("Inconsistent probabilities")
		return False

compareActions(a1,a2)


