""" 
This program takes a running total of the count (number of child nodes), the mean and LOvariance and a new sample value and updates the running estimation of those two values given the new sample. It also requires a 
"""

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
    Mnew = cMean + (newValue-cMean)/count
    cVariance = cVariance + (newValue-cMean)*(newValue-Mnew)
    cMean = Mnew
    if(count > 1):
        cVariance = cVariance/(count-1)
    else:
        cVariance = 0
    
    return cMean, cVariance
 

