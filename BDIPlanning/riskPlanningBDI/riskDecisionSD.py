'''
The is the same a riskdivision.py except we use a differnt measure to calculate the best action, namely the percentage confidence that the outcoem wil be in a range R. Where r is simply a ration of the mean and the range is this ratio applied to the mean aroud the mean
'''

from __future__ import division
import math
import random


cResource = 100 #this should have a negative correlation with R

class Action():
    def __init__(self, name, utility, risk):
        self.name = name
        self.utility = utility
        self.risk = risk

    def __repr__(self):
        return self.name + ", "+ str(self.utility) + ", "+ str(self.risk)
            
'''
a0 = Action("a0", 40, 450)
a1 = Action("a1", 33, 270)
a2 = Action("a2", 19, 150)
a3 = Action("a3", 18 , 50 )
a4 = Action("a4", 9, 24)
a5 = Action("a5", 1, 10)
'''




a0 = Action("a0", 300, 1100)
a1 = Action("a1", 290, 270)
a2 = Action("a2", 250, 246)
a3 = Action("a3", 111 , 220 )
a4 = Action("a4", 90, 24)
a5 = Action("a5", 43, 6)

aList = [a0,a1,a2,a3,a4,a5]

#Generate a set of 5 random actions within the constraint rules
def generateActions():
    global aList
    aList = []
    for i in range(5):
        if(i == 0):
            aList.append(Action("a0", random.randint(0,9999), random.randint(0,9999)))
        else:
            aList.append(Action("a"+str(i), random.randint(0,aList[i-1].utility), random.randint(0,aList[i-1].risk)))


#Takes a confidence level in sigma and converts it to percentage confidence
#This uses the formula of an error function fed with the (sigma /  the sqrt of 2) 
def sigmaToPercent(sigma):
    confidence = math.erf(sigma / math.sqrt(2))
    return confidence * 100

#This calculates the average utility across all actions, this is used as our absolute value to alter risk tolerance
def getAvg():
    total = 0
    for a in aList: 

        total += a.risk



    return total/len(aList)


def pickAction(R):
    avg = getAvg()
    print("avgSD "+str(avg))   

    topActionConf = 0       #the highest percentage confidence so far
    topAction = 0
    for i in range (len(aList)):
        #calculate the tolerance range (just calculate the top one, doesnt matter either way)
        SD = math.sqrt(aList[i].risk)  #calc the standard deviation

        trange = (aList[i].utility*R)+(aList[i].utility**(R*10))        
        
        confidence = (trange / SD)	#calc th confidence in sigmas (standard deviations)
        #confidence = sigmaToPercent(confidence)	#calculate the confidence in %
        print "Confidence that "+aList[i].name+" is in interval "+ str(aList[i].utility) +"+-"+ str(trange)+" is "+ str(confidence) +" sigma"
        if(confidence > topActionConf):
            topActionConf = confidence		
            topAction = i
    #find top percentage and return as the selected action

	    
    print(topAction)
    return topAction









'''
#old, non adjustable decsions
def pickAction(R):
    print("R= "+str(R))

    avg = getAvg()
    
    topActionConf = 0       #the highest percentage confidence so far
    topAction = 0
    for i in range (len(aList)):
        #calculate the tolerance range (just calculate the top one, doesnt matter either way)
        SD = math.sqrt(aList[i].risk)  #calc the standard deviation
        trange = aList[i].utility*R        
                 
        confidence = (trange / SD)	#calc th confidence in sigmas (standard deviations)
        #confidence = sigmaToPercent(confidence)	#calculate the confidence in %
        print "Confidence that "+aList[i].name+" is in interval "+ str(aList[i].utility) +"+-"+ str(trange)+" is "+ str(confidence) +"sigma"
        if(confidence > topActionConf):
            topActionConf = confidence		
            topAction = i

    #find top percentage and return as the selected action
	    
    print(topAction)
    return topAction
'''

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
