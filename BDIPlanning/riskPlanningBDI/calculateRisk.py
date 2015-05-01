""" 
This program takes a running total of the count (number of child nodes), the mean and LOvariance and a new sample value and updates the running estimation of those two values given the new sample. It also requires a 
"""

from __future__ import division
import random

def updateLOVariance(count, cMean, cVariance, newValue):
    if(newValue < 0):
        Mnew = cMean + (newValue-cMean)/count
        cVariance = cVariance + (newValue-cMean)*(newValue-Mnew)
        cMean = Mnew

        if(count > 1):
            cVariance = cVariance/(count-1)
        
        return cMean, cVariance
    else:
        return cMean, cVariance


def updateVariance(count, cMean, cVariance, newValue):

    if(count > 1):
        Mnew = cMean + (newValue-cMean)/count
        cVariance = cVariance + (newValue-cMean)*(newValue-Mnew)
        cMean = Mnew
        cVariance = cVariance/(count-1)
    else:
        cMean = newValue
        cVariance = 0
    
    return cMean, cVariance
 
def updateVariance2(count, cMean, M2, newValue):
			
	delta = newValue - cMean
	mean = cMean + delta/count
	M2 = M2 + delta*(newValue - mean)

	if(count < 2):
		return mean, M2, 0

	variance = M2/(count-1)
	return mean, M2, variance
	

def test():
	x = 0
	y = 0
	for i in range(10000):
		r = random.randint(0,99)
		if(r<80):
			x,y,z = updateVariance2(i+1, x, y, -30)
		else:
			x,y,z = updateVariance2(i+1, x, y, -100)
		print x,y,z
		
test()	
