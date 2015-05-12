from __future__ import division
import math

class AssessedAction():
	def __init__(self, name, utility, risk):
		self.name = name
		self.utility = utility
		self.risk = risk

#Takes a list of actions and returns (the index of) the best one based ona rsk aware decision strategy
#The decision strategy sued here is the confidence interval approach
def rankRiskAwareCI(aList):

    AAList, lowestU = generateAAList(aList)

    topActionConf = None       #the highest percentage confidence so far
    topAction = None
    for i in range (len(AAList)):
        #calculate the tolerance range (just calculate the top one, doesnt matter either way)
        SD = math.sqrt(AAList[i].risk)  #calc the standard deviation
        
        utility = AAList[i].utility 
        trange = (utility - lowestU) +1	#This normalises all values to be above zero
        
        if(SD > 0):
        	confidence = (trange / SD)  #calc th confidence in sigmas (standard deviations)
        else:
            confidence = float('inf') #if the SD is 0, then our confidence in its interval will be infinite

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

#The list will be ranked by utility, but there could be actions in the list which have both lower utiltiy and higher risk than their predecessor. These actions are obviously not desirable, so remove them.
#This satisfies the postulate: "We are only interested in actions with lower utilties if they also have lower risk"
def removeRedundantActions(AAList):
	
	i = 1
	for x in range(len(AAList) -1):
		print i
		if(AAList[i].risk > AAList[i-1].risk):
			print "Removing "+AAList[i].name + " from options as it has higher risk than a better option"
			AAList.remove(AAList[i])
			i -= 1		#we've just removed an item, so set the index back to scan the next item
		i += 1
	return AAList


#Same as above but using the ratio approach, also normalises the utility values to be non-negative, not sure about this practice yet
def rankRiskAwareRatio(aList, R):
	AAList, lowestU = generateAAList(aList)

	AAList = removeRedundantActions(AAList)

	#normalise to 0
	#for aa in AAList:
	#	aa.utility = aa.utility - lowestU

	selectedAction = 0  #first action selectedd by default
	for i in range(len(AAList)-1):
		uRatio = (AAList[i].utility-AAList[i+1].utility) / AAList[i].utility
		#print(uRatio)
		rRatio = (AAList[i].risk-AAList[i+1].risk) / AAList[i].risk
		print("Ratio "+ AAList[i].name +":"+ AAList[i+1].name +" | "+ str(uRatio) +", "+ str(rRatio))	
		if(rRatio * R >= uRatio):
			selectedAction = i+1
		else:
			return selectedAction
	#print(selectedAction)
	return selectedAction



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

	
                       

