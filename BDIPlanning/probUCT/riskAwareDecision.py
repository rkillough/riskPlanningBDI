from __future__ import division
import math


#Takes a list of actions and returns the best one based ona rsk aware decision strategy
def rankRiskAware(aList):

    aList = normaliseUtility(aList)

    topActionConf = None       #the highest percentage confidence so far
    topAction = None
    for i in range (len(aList)):
        #calculate the tolerance range (just calculate the top one, doesnt matter either way)
        SD = math.sqrt(aList[i].risk)  #calc the standard deviation
        
        utility = aList[i].utility / aList[i].visits
        trange = utility

        confidence = (trange / SD)  #calc th confidence in sigmas (standard deviations)
     
        print "Confidence that "+aList[i].action.name+" is in interval "+ str(utility) +"+-"+ str(trange)+" is "+ str(confidence) +"%"
 
        if(topAction == None):
            topActionConf = confidence
            topAction = i
        if(confidence > topActionConf):
            topActionConf = confidence
            topAction = i
    #find top percentage and return as the selected action

    #print(topAction)
    return topAction

#The confidence calcluation does not handle negative utility values, so normalise all value to be >0
#by adding teh value of the lowest utility to all the utilities
#returns a list of utilities anf risk, the rest is discarded
def normaliseUtility(actions):
    lowestUtility = 0		#if no utilities are below zero, we wont need to do anything so well just be adding this 0

    newList = []
    
    for a in actions:
        u = a.utility/a.visits
        if(u < lowestUtility):
            lowestUtility = u

    for a in actions:
        newList.append((a.utility/a.visits) - )
                       

