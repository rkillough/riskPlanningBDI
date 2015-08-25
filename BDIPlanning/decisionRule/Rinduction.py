#resources - set of amounts of remaining resources
#weights  - corresponding value of the resources
#requirments - corresponding amounts of resources needed to complete the goal from this point

'''
The procedure is to calculate a "scarcity measure" from the amoutn we have vs the amount we need, this is then modulated by the weight assigned, giving an indication of how much we value the resource. The values for each resource are then combined and constrained to within a 0 to maxR range. Where maxR is the maximum useful R, i.e. the point at which the probability of success is maximised.
'''

class resource():
	__init__(supply, demand, weight, scarcity):
		self.supply = supply #amount of the resource available
		self.demand = demand #amount of resource required to reach goal
		self.weight = weight #the external value of this resource (as a [0,1] where all weights add to 1)
		self.scarcity = self.calcScarcity()	#a measure of the scarcity based on supply & demand

	def calcScarcity():
		if self.demand == 0: return 0		#no demand, no scarcity
		elif self.demand > self.supply: return 0	#demand exceeds supply, give up
		else: return 1/(self.supply/self.demand)

def getR(resources, maxR):
	total = 0

	for r in resources:
		total += (r.value * maxR) * r.scarcity
	R = total
	print R

maxR = 5
resources = [3,10]
weights = [0.6, 0.1]
getR(weights, resources, maxR)
