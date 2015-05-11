from __future__ import division
import math

class AssessedAction():
	def __init__(self, name, utility, risk):
		self.name = name
		self.utility = utility
		self.risk = risk

#Takes a list of actions and returns the best one based ona rsk aware decision strategy
def rankRiskAware(aList):

    AAList, lowestU = generateAAList(aList)

    topActionConf = None       #the highest percentage confidence so far
    topAction = None
    for i in range (len(AAList)):
        #calculate the tolerance range (just calculate the top one, doesnt matter either way)
        SD = math.sqrt(AAList[i].risk)  #calc the standard deviation
        
        utility = AAList[i].utility 
        trange = utility - lowestU	#This normalises all values to be above zero

        confidence = (trange / SD)  #calc th confidence in sigmas (standard deviations)
     
        print "Confidence that "+aList[i].action.name+" is in interval "+ str(utility) +"+-"+ str(trange)+" is "+ str(confidence) +"sigma"
 
        if(topAction == None):
            topActionConf = confidence
            topAction = i
        if(confidence > topActionConf):
            topActionConf = confidence
            topAction = i
    #find top percentage and return as the selected action

    #print(topAction)
    return topAction

#The confidence calcluation does not handle negative utility values, work out the lweest utility for later normalisation by adding teh value of the lowest utility to all the utilities, this is done in the rankigng proces

#This method has a dual purpose, to determine the lowest utility so that the confidence range cam be normalised to >0. It also generates a list of assessed actions from the passed node list which just contains the name, utility an risk of each action.
def generateAAList(actions):
    lowestUtility = 0		#if no utilities are below zero, we wont need to do anything so well just be adding this 0
    newList = []
    
    for a in actions:
        u = a.utility/a.visits
        if(u < lowestUtility):
            lowestUtility = u

    for a in actions:
		aa = AssessedAction(a.action.name, (a.utility/a.visits), a.risk)
		newList.append(aa)

    return newList, lowestUtility

	
                       

