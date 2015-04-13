'''
The is the same a riskdivision.py except we use a differnt measure to calculate the best action, namely the percentage confidence that the outcoem wil be in a range R. Where r is simply a ration of the mean and the range is this ratio applied to the mean aroud the mean
'''

from __future__ import division
import math

cResource = 100 #this should have a negative correlation with R

class Action():
    def __init__(self, name, utility, risk):
        self.name = name
        self.utility = utility
        self.risk = risk

    def __repr__(self):
        return self.name + ", "+ str(self.utility) + ", "+ str(self.risk)
            

a0 = Action("a0", 40, 450)
a1 = Action("a1", 33, 270)
a2 = Action("a2", 19, 150)
a3 = Action("a3", 18 , 50 )
a4 = Action("a4", 9, 24)
a5 = Action("a5", 1, 10)
a6 = Action("a6", -22, 1)

aList = [a0,a1,a2,a3,a4,a5,a6]


#Takes a confidence level in sigma and converts it to percentage confidence
#This uses the formula of an error function fed with the (sigma /  the sqrt of 2) 
def sigmaToPercent(sigma):
    confidence = math.erf(sigma / math.sqrt(2))
    return confidence * 100

def pickAction(R):
    print("R= "+str(R))
    
    topActionConf = 0       #the highest percentage confidence so far
    topAction = 0
    for i in range (len(aList)):
        #calculate the tolerance range (just calculate the top one, doesnt matter either way)
        trange = R * aList[i].utility
        SD = math.sqrt(aList[i].risk)  #calc the standard deviation
        confidence = (trange / SD)	#calc th confidence in sigmas (standard deviations)
        confidence = sigmaToPercent(confidence)	#calculate the confidence in %
        print "Confidence that "+aList[i].name+" is in interval "+ str(aList[i].utility) +"+-"+ str(trange)+" is "+ str(confidence) +"%"
        if(confidence > topActionConf):
            topActionConf = confidence		
            topAction = i
    #find top percentage and return as the selected action
	    


    print(topAction)
    return topAction

def getActions():
	return aList        

def adjustRiskTolerance():
    R=1 

    for i in range(100):
        print(R)
        print(pickAction(R))
        print
        R = R - 0.01

#adjustRiskTolerance()
#print(adjustRiskTolerance())
